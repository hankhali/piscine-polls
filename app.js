'use strict';

// In-memory state loaded from backend API
let state = { polls: [] };

async function apiGetPolls() {
  const res = await fetch('/api/polls');
  if (!res.ok) throw new Error('Failed to load polls');
  const data = await res.json();
  
  // Sort polls by the number in their title (e.g., "1. Best Staff", "2. Volume Icon")
  const polls = data.polls || [];
  polls.sort((a, b) => {
    // Extract the number from the title (e.g., "1." or "2.")
    const numA = parseInt(a.title.match(/(\d+)\./)?.[1] || '999');
    const numB = parseInt(b.title.match(/(\d+)\./)?.[1] || '999');
    return numA - numB;
  });
  
  state.polls = polls;
}

async function apiCreatePoll({ title, description, poll_type, options }) {
  console.log('Creating poll:', { title, description, poll_type, options });
  const res = await fetch('/api/polls', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description, poll_type, options }),
  });
  console.log('Response status:', res.status);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    console.error('Error response:', err);
    alert(err.error || 'Failed to create poll');
    return;
  }
  const result = await res.json();
  console.log('Poll created successfully:', result);
  await apiGetPolls();
}

async function apiDeletePoll(pollId) {
  const res = await fetch(`/api/polls/${pollId}`, { method: 'DELETE' });
  if (!res.ok) {
    alert('Failed to delete poll');
    return;
  }
  await apiGetPolls();
}

async function apiUpdatePoll(pollId, data) {
  console.log('Updating poll:', pollId, 'with data:', data);
  const res = await fetch(`/api/polls/${pollId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    alert(err.error || 'Failed to update poll');
    return false;
  }
  await apiGetPolls();
  return true;
}

async function apiCastVote(pollId, optionId, username) {
  const res = await fetch(`/api/polls/${pollId}/vote`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ option_id: optionId, username }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    alert(err.error || 'Failed to cast vote');
    return;
  }
  await apiGetPolls();
}

async function apiSubmitTextResponse(pollId, responseText, username) {
  const res = await fetch(`/api/polls/${pollId}/text-response`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ response_text: responseText, username }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    alert(err.error || 'Failed to submit response');
    return;
  }
  await apiGetPolls();
}

async function apiGetPollVotes(pollId) {
  const res = await fetch(`/api/polls/${pollId}/votes`);
  if (!res.ok) return { votes: [] };
  return res.json();
}

function totalVotes(poll) {
  return poll.options.reduce((sum, o) => sum + (o.votes || 0), 0);
}

// UI rendering
const appRoot = document.getElementById('app');

const ROLE = (window.APP_ROLE === 'admin' ? 'admin' : 'student');
let currentView = ROLE; // fixed per page
const USERNAME_KEY = 'polls-intra-username';
let currentUsername = localStorage.getItem(USERNAME_KEY) || '';

function formatShortId(id) {
  const s = String(id);
  return s.slice(-6);
}

function createElement(tag, className, children) {
  const el = document.createElement(tag);
  if (className) el.className = className;
  if (children !== undefined) {
    if (Array.isArray(children)) {
      children.forEach((child) => {
        if (typeof child === 'string') el.appendChild(document.createTextNode(child));
        else if (child) el.appendChild(child);
      });
    } else if (typeof children === 'string') {
      el.appendChild(document.createTextNode(children));
    } else if (children) {
      el.appendChild(children);
    }
  }
  return el;
}

function renderHeader() {
  // Used only for admin layout now
  const title = createElement('div', 'app-title', 'Polls');
  const labelEl = createElement('div', 'section-title', 'Admin Portal');
  const header = createElement('div', 'app-header', [title, labelEl]);
  return header;
}

function showEditPollDialog(poll) {
  console.log('Opening edit dialog for poll:', poll);
  
  // Create modal overlay
  const overlay = createElement('div', 'modal-overlay');
  
  // Create modal content
  const modal = createElement('div', 'modal-content');
  const modalHeader = createElement('div', 'modal-header', 'Edit Poll');
  
  const form = createElement('form', 'edit-poll-form');
  
  const titleGroup = createElement('div', 'form-group');
  const titleLabel = createElement('label', null, 'Poll Title');
  const titleInput = createElement('input');
  titleInput.type = 'text';
  titleInput.value = poll.title;
  titleInput.required = true;
  titleGroup.appendChild(titleLabel);
  titleGroup.appendChild(titleInput);
  
  const descGroup = createElement('div', 'form-group');
  const descLabel = createElement('label', null, 'Description');
  const descInput = createElement('textarea');
  descInput.rows = 3;
  descInput.value = poll.description || '';
  descGroup.appendChild(descLabel);
  descGroup.appendChild(descInput);
  
  // Add poll type selection
  const typeGroup = createElement('div', 'form-group');
  const typeLabel = createElement('label', null, 'Poll Type');
  const typeSelect = createElement('select');
  
  const optionMultiple = createElement('option', null, 'Multiple Choice');
  optionMultiple.value = 'multiple_choice';
  const optionText = createElement('option', null, 'Text Response');
  optionText.value = 'text_response';
  
  typeSelect.appendChild(optionMultiple);
  typeSelect.appendChild(optionText);
  typeSelect.value = poll.poll_type || 'multiple_choice';
  
  typeGroup.appendChild(typeLabel);
  typeGroup.appendChild(typeSelect);
  
  // Options container (show/hide based on poll type)
  const optionsContainer = createElement('div', 'form-group');
  const optionsLabel = createElement('label', null, 'Options');
  optionsContainer.appendChild(optionsLabel);
  
  const optionsList = createElement('div', 'options-list');
  optionsContainer.appendChild(optionsList);
  
  const addOptionBtn = createElement('button', 'button button-secondary', '+ Add Option');
  addOptionBtn.type = 'button';
  optionsContainer.appendChild(addOptionBtn);
  
  // Function to add option input
  function addOptionInput(value = '') {
    const optionRow = createElement('div', 'option-row');
    const optionInput = createElement('input');
    optionInput.type = 'text';
    optionInput.placeholder = 'Option name';
    optionInput.value = value;
    optionInput.className = 'option-input';
    
    const removeBtn = createElement('button', 'button-remove', '×');
    removeBtn.type = 'button';
    removeBtn.onclick = () => optionsList.removeChild(optionRow);
    
    optionRow.appendChild(optionInput);
    optionRow.appendChild(removeBtn);
    optionsList.appendChild(optionRow);
  }
  
  // Populate existing options
  if (poll.options && poll.options.length > 0) {
    poll.options.forEach(opt => addOptionInput(opt.name));
  } else {
    addOptionInput();
    addOptionInput();
  }
  
  addOptionBtn.onclick = () => addOptionInput();
  
  // Toggle options visibility based on poll type
  function updateOptionsVisibility() {
    optionsContainer.style.display = typeSelect.value === 'multiple_choice' ? 'block' : 'none';
  }
  updateOptionsVisibility();
  typeSelect.onchange = updateOptionsVisibility;
  
  const buttonGroup = createElement('div', 'modal-buttons');
  const cancelBtn = createElement('button', 'button button-secondary', 'Cancel');
  cancelBtn.type = 'button';
  cancelBtn.onclick = () => document.body.removeChild(overlay);
  
  const saveBtn = createElement('button', 'button button-primary', 'Save Changes');
  saveBtn.type = 'submit';
  
  buttonGroup.appendChild(cancelBtn);
  buttonGroup.appendChild(saveBtn);
  
  form.appendChild(titleGroup);
  form.appendChild(descGroup);
  form.appendChild(typeGroup);
  form.appendChild(optionsContainer);
  form.appendChild(buttonGroup);
  
  form.onsubmit = async (e) => {
    e.preventDefault();
    const title = titleInput.value.trim();
    const description = descInput.value.trim();
    const poll_type = typeSelect.value;
    
    if (!title) {
      alert('Title is required');
      return;
    }
    
    const data = { title, description, poll_type };
    
    // Collect options if multiple_choice
    if (poll_type === 'multiple_choice') {
      const options = Array.from(optionsList.querySelectorAll('.option-input'))
        .map(input => input.value.trim())
        .filter(val => val);
      
      if (options.length < 2) {
        alert('Please provide at least 2 options for multiple choice polls');
        return;
      }
      
      data.options = options;
    }
    
    const success = await apiUpdatePoll(poll.id, data);
    if (success) {
      document.body.removeChild(overlay);
      render();
    }
  };
  
  modal.appendChild(modalHeader);
  modal.appendChild(form);
  overlay.appendChild(modal);
  
  overlay.onclick = (e) => {
    if (e.target === overlay) {
      document.body.removeChild(overlay);
    }
  };
  
  document.body.appendChild(overlay);
  titleInput.focus();
}

function renderCreatePollForm() {
  const form = createElement('form', 'form-card');

  const actionsRow = createElement('div', 'section-header');
  const leftText = createElement('div', null, 'Create New Poll');
  const createBtn = createElement('button', 'button button-primary', 'Save Poll');
  createBtn.type = 'submit';
  actionsRow.appendChild(leftText);
  actionsRow.appendChild(createBtn);

  const titleGroup = createElement('div', 'form-group');
  const titleLabel = createElement('label', null, 'Poll title');
  const titleInput = createElement('input');
  titleInput.type = 'text';
  titleInput.required = true;
  titleInput.placeholder = 'Enter poll title...';
  titleGroup.appendChild(titleLabel);
  titleGroup.appendChild(titleInput);

  const descGroup = createElement('div', 'form-group');
  const descLabel = createElement('label', null, 'Description');
  const descInput = createElement('textarea');
  descInput.rows = 2;
  descInput.placeholder = 'Optional description...';
  descGroup.appendChild(descLabel);
  descGroup.appendChild(descInput);

  // Add poll type selection
  const typeGroup = createElement('div', 'form-group');
  const typeLabel = createElement('label', null, 'Poll Type');
  const typeSelect = createElement('select');
  
  const optionMultiple = createElement('option', null, 'Multiple Choice');
  optionMultiple.value = 'multiple_choice';
  const optionText = createElement('option', null, 'Text Response');
  optionText.value = 'text_response';
  
  typeSelect.appendChild(optionMultiple);
  typeSelect.appendChild(optionText);
  
  typeGroup.appendChild(typeLabel);
  typeGroup.appendChild(typeSelect);

  const optionsGroup = createElement('div', 'form-group');
  const optionsLabel = createElement('label', null, 'Options (one per line)');
  const optionsInput = createElement('textarea');
  optionsInput.rows = 4;
  optionsInput.placeholder = 'Option 1\nOption 2\nOption 3...';
  optionsGroup.appendChild(optionsLabel);
  optionsGroup.appendChild(optionsInput);

  // Toggle options visibility based on poll type
  function updateOptionsVisibility() {
    optionsGroup.style.display = typeSelect.value === 'multiple_choice' ? 'block' : 'none';
  }
  
  typeSelect.addEventListener('change', updateOptionsVisibility);
  updateOptionsVisibility();

  form.appendChild(actionsRow);
  form.appendChild(titleGroup);
  form.appendChild(descGroup);
  form.appendChild(typeGroup);
  form.appendChild(optionsGroup);

  form.onsubmit = function (e) {
    e.preventDefault();
    const title = titleInput.value.trim();
    const description = descInput.value.trim();
    const poll_type = typeSelect.value;
    const optionsRaw = optionsInput.value
      .split('\n')
      .map((s) => s.trim())
      .filter(Boolean);

    if (!title) {
      alert('Please enter a title.');
      return;
    }

    if (poll_type === 'multiple_choice' && optionsRaw.length < 2) {
      alert('Please enter at least two options for multiple choice polls.');
      return;
    }

    apiCreatePoll({ title, description, poll_type, options: optionsRaw })
      .then(() => {
        titleInput.value = '';
        descInput.value = '';
        optionsInput.value = '';
        typeSelect.value = 'multiple_choice';
        updateOptionsVisibility();
        render();
      })
      .catch(() => {
        alert('Failed to create poll');
      });
  };

  return form;
}

function renderPollCard(poll, forAdmin) {
  const total = totalVotes(poll);

  if (forAdmin) {
    // Admin management card: compact white-ish card with delete + View
    const card = createElement('div', 'admin-poll-card');

    const title = createElement('div', 'admin-poll-title', poll.title);
    const deleteBtn = (function () {
      const btn = createElement('button', 'admin-delete-btn', '🗑');
      btn.title = 'Delete poll';
      btn.onclick = () => {
        if (confirm('Delete this poll?')) {
          apiDeletePoll(poll.id)
            .then(() => render())
            .catch(() => alert('Failed to delete poll'));
        }
      };
      return btn;
    })();

    const header = createElement('div', 'admin-poll-header', [title, deleteBtn]);

    const desc = poll.description
      ? createElement('div', 'admin-poll-desc', poll.description)
      : createElement('div', 'admin-poll-desc', '');

    // Add bar chart visualization (only for multiple choice)
    const chartContainer = createElement('div', 'admin-chart-container');
    
    if (poll.poll_type === 'text_response') {
      const textInfo = createElement('div', 'admin-chart-title', '📝 Text Response Poll');
      const textDesc = createElement('div', 'admin-chart-empty', 'Students write their own responses');
      chartContainer.appendChild(textInfo);
      chartContainer.appendChild(textDesc);
    } else {
      const chartTitle = createElement('div', 'admin-chart-title', '📊 Results');
      chartContainer.appendChild(chartTitle);
      
      if (total > 0 && poll.options) {
        const sortedOptions = [...poll.options].sort((a, b) => b.votes - a.votes);
        sortedOptions.forEach((option, index) => {
          const percentage = total > 0 ? (option.votes / total * 100) : 0;
          
          const barRow = createElement('div', 'admin-bar-row');
        const barLabel = createElement('div', 'admin-bar-label', option.name);
        const barContainer = createElement('div', 'admin-bar-container');
        const barFill = createElement('div', 'admin-bar-fill');
        barFill.style.width = percentage + '%';
        
        // Color the top option differently
        if (index === 0 && option.votes > 0) {
          barFill.classList.add('admin-bar-fill-winner');
        }
        
        const barValue = createElement('div', 'admin-bar-value', `${option.votes} (${percentage.toFixed(1)}%)`);
        
        barContainer.appendChild(barFill);
        barRow.appendChild(barLabel);
        barRow.appendChild(barContainer);
        barRow.appendChild(barValue);
        chartContainer.appendChild(barRow);
      });
      } else {
        const noVotes = createElement('div', 'admin-chart-empty', 'No votes yet');
        chartContainer.appendChild(noVotes);
      }
    }

    const info = createElement('div', 'admin-poll-meta-row', [
      createElement('div', 'admin-poll-meta', [
        createElement('span', 'admin-meta-icon', poll.poll_type === 'text_response' ? '📝' : '👤'),
        createElement('span', null, poll.poll_type === 'text_response' ? 'Text Response' : `${poll.options.length} candidates`),
      ]),
      createElement('div', 'admin-poll-meta', [
        createElement('span', 'admin-meta-icon', '✅'),
        createElement('span', null, `${total} ${poll.poll_type === 'text_response' ? 'responses' : 'votes'}`),
      ]),
    ]);

    const idLabel = createElement('div', 'admin-poll-id', 'ID: ' + formatShortId(poll.id));

    const editBtn = createElement('button', 'admin-edit-btn', '✏️ Edit');
    editBtn.type = 'button';
    editBtn.onclick = () => showEditPollDialog(poll);

    const viewVotesBtn = createElement('button', 'admin-view-btn', 'View ▸');
    viewVotesBtn.type = 'button';

    const exportBtn = createElement('button', 'admin-export-btn', '📥 CSV');
    exportBtn.type = 'button';
    exportBtn.title = 'Export votes to CSV';
    exportBtn.onclick = () => {
      window.location.href = `/api/polls/${poll.id}/votes/export`;
    };

    const buttonGroup = createElement('div', 'admin-button-group', [editBtn, viewVotesBtn, exportBtn]);

    const footer = createElement('div', 'admin-poll-footer', [idLabel, buttonGroup]);

    const votesContainer = createElement('div', 'admin-votes-container');

    viewVotesBtn.onclick = () => toggleAdminVotes(poll.id, votesContainer, viewVotesBtn);

    card.appendChild(header);
    card.appendChild(desc);
    card.appendChild(chartContainer);
    card.appendChild(info);
    card.appendChild(footer);
    card.appendChild(votesContainer);
    return card;
  }

  // Student-facing 42-style card (collapsed by default, expand to see options)
  const card = createElement('div', 'poll-card poll-card-cyan');

  const headerBg = createElement('div', 'poll-card-header-bg', '42');
  const idBadge = createElement('div', 'poll-id-badge', '#' + poll.id);
  const titleEl = createElement('h3', 'poll-title', poll.title);
  const descEl = createElement('p', 'poll-description', poll.description || '');
  const headerContent = createElement('div', 'poll-card-header-content', [idBadge, titleEl, descEl]);
  const header = createElement('div', 'poll-card-header poll-card-header-cyan', [headerBg, headerContent]);

  const stats = createElement('div', 'poll-stats', [
    (function () {
      const box = createElement('div', 'poll-stat');
      const label = poll.poll_type === 'text_response' ? 'TYPE' : 'CAND';
      const value = poll.poll_type === 'text_response' ? 'TEXT' : String(poll.options.length);
      box.appendChild(createElement('div', 'poll-stat-label stat-label-cyan', label));
      box.appendChild(createElement('div', 'poll-stat-value', value));
      return box;
    })(),
    (function () {
      const box = createElement('div', 'poll-stat');
      const label = poll.poll_type === 'text_response' ? 'RESP' : 'VOTES';
      box.appendChild(createElement('div', 'poll-stat-label stat-label-cyan', label));
      box.appendChild(createElement('div', 'poll-stat-value', '•••'));
      return box;
    })(),
    (function () {
      const box = createElement('div', 'poll-stat');
      box.appendChild(createElement('div', 'poll-stat-label stat-label-cyan', 'TIME'));
      box.appendChild(createElement('div', 'poll-stat-value', poll.closesLabel || '')); 
      return box;
    })(),
  ]);

  const votedKey = `poll-voted-${poll.id}-${currentUsername || 'anon'}`;
  const alreadyVoted = !!localStorage.getItem(votedKey);
  let selectedId = null;

  const candidatesList = createElement('div', 'candidates-list');
  
  // Handle text response polls
  if (poll.poll_type === 'text_response') {
    if (alreadyVoted) {
      const thankYou = createElement('div', 'text-response-submitted', '✅ Thank you for your response!');
      candidatesList.appendChild(thankYou);
    } else {
      const textInput = createElement('textarea');
      textInput.className = 'text-response-input';
      textInput.placeholder = 'Type your response here...';
      textInput.rows = 5;
      candidatesList.appendChild(textInput);
    }
  }
  // Handle multiple choice polls
  else if (poll.options && poll.options.length > 0) {
    // Add thank you message if user has voted
    if (alreadyVoted) {
      const thankYou = createElement('div', 'text-response-submitted', '✅ Thank you for voting!');
      candidatesList.appendChild(thankYou);
    } else {
      // Show voting buttons if not voted yet
      poll.options.forEach((option) => {
        const btn = createElement('button', 'candidate-button candidate-button-cyan', null);
        btn.type = 'button';
        if (alreadyVoted) {
          btn.disabled = true;
        }

        const checkbox = createElement('div', 'candidate-checkbox');
        const dot = createElement('div', 'candidate-checkbox-dot checkbox-dot-cyan');
        checkbox.appendChild(dot);

        const label = createElement('span', null, option.name);
        const content = createElement('div', 'candidate-content', [checkbox, label]);
        btn.appendChild(content);

        btn.onclick = () => {
          if (alreadyVoted) return;
          selectedId = option.id;
          Array.from(candidatesList.querySelectorAll('.candidate-button')).forEach((b) => {
            b.classList.remove('selected', 'candidate-button-cyan');
          });
          btn.classList.add('selected', 'candidate-button-cyan');
        };

        candidatesList.appendChild(btn);
      });
    }
  }

  const details = createElement('div', 'poll-details');
  const candidatesWrapper = createElement('div', 'poll-candidates', [candidatesList]);

  const footer = createElement('div', 'poll-card-footer poll-card-footer-cyan');
  const voteBtn = createElement(
    'button',
    'vote-button vote-button-cyan',
    alreadyVoted ? 'VOTED' : '> VOTE'
  );
  voteBtn.type = 'button';
  if (alreadyVoted) {
    voteBtn.disabled = true;
  }

  voteBtn.onclick = () => {
    if (alreadyVoted) return;
    
    // Handle text response submission
    if (poll.poll_type === 'text_response') {
      const textInput = candidatesList.querySelector('.text-response-input');
      const responseText = textInput ? textInput.value.trim() : '';
      
      if (!responseText) {
        alert('Please enter your response before submitting.');
        return;
      }
      
      apiSubmitTextResponse(poll.id, responseText, currentUsername)
        .then(() => {
          localStorage.setItem(votedKey, '1');
          render();
        })
        .catch(() => alert('Failed to submit response'));
    }
    // Handle multiple choice vote
    else {
      if (!selectedId) {
        alert('Please select a candidate before voting.');
        return;
      }
      apiCastVote(poll.id, selectedId, currentUsername)
        .then(() => {
          localStorage.setItem(votedKey, '1');
          render();
        })
        .catch(() => alert('Failed to cast vote'));
    }
  };

  footer.appendChild(createElement('div', 'poll-status', 'STATUS: ACTIVE'));
  footer.appendChild(voteBtn);

  details.appendChild(candidatesWrapper);
  details.appendChild(footer);
  details.style.display = 'none';

  const toggleRow = createElement('div', 'poll-toggle-row');
  const viewBtn = createElement('button', 'view-details-btn', 'View ▸');
  viewBtn.type = 'button';
  viewBtn.onclick = () => {
    const isOpen = details.style.display === 'block';
    
    if (!isOpen) {
      // Close all other open poll details first
      document.querySelectorAll('.poll-details').forEach(otherDetails => {
        if (otherDetails !== details && otherDetails.style.display === 'block') {
          otherDetails.style.display = 'none';
          // Find and reset the corresponding View button
          const parentCard = otherDetails.closest('.poll-card');
          if (parentCard) {
            const otherBtn = parentCard.querySelector('.view-details-btn');
            if (otherBtn) otherBtn.textContent = 'View ▸';
          }
        }
      });
    }
    
    details.style.display = isOpen ? 'none' : 'block';
    viewBtn.textContent = isOpen ? 'View ▸' : 'Hide ▾';
  };
  toggleRow.appendChild(viewBtn);

  card.appendChild(header);
  card.appendChild(stats);
  card.appendChild(toggleRow);
  card.appendChild(details);

  return card;
}

function renderVoteOptions(poll) {
  const container = createElement('div', 'vote-options');
  const votedKey = `poll-voted-${poll.id}-${currentUsername || 'anon'}`;
  const alreadyVoted = !!localStorage.getItem(votedKey);

  let selectedId = null;

  poll.options.forEach((option) => {
    const label = `${option.name} (${option.votes || 0} votes)`;
    const btn = createElement('button', 'vote-option-button', label);
    btn.type = 'button';
    if (alreadyVoted) {
      btn.disabled = true;
    }
    btn.onclick = () => {
      if (alreadyVoted) return;
      selectedId = option.id;
      // highlight selection
      Array.from(container.querySelectorAll('.vote-option-button')).forEach((b) => {
        b.classList.remove('selected');
      });
      btn.classList.add('selected');
    };
    container.appendChild(btn);
  });

  const submitRow = createElement('div', 'vote-submit-row');
  const submitBtn = createElement('button', 'button button-primary', alreadyVoted ? 'You have already voted' : 'Submit Vote');
  submitBtn.type = 'button';
  if (alreadyVoted) {
    submitBtn.disabled = true;
  }

  submitBtn.onclick = () => {
    if (alreadyVoted) return;
    if (!selectedId) {
      alert('Please select a candidate before submitting your vote.');
      return;
    }
    apiCastVote(poll.id, selectedId)
      .then(() => {
        localStorage.setItem(votedKey, '1');
        alert('Your vote has been recorded. Thank you for participating.');
        render();
      })
      .catch(() => alert('Failed to cast vote'));
  };

  submitRow.appendChild(submitBtn);
  container.appendChild(submitRow);

  return container;
}

async function toggleAdminVotes(pollId, container, buttonEl) {
  // If this card is already open, close it
  if (container.dataset.open === '1') {
    container.innerHTML = '';
    container.dataset.open = '0';
    if (buttonEl) buttonEl.textContent = 'View ▸';
    return;
  }

  // Close all other open vote containers first
  const allContainers = document.querySelectorAll('.admin-votes-container[data-open="1"]');
  allContainers.forEach(otherContainer => {
    if (otherContainer !== container) {
      otherContainer.innerHTML = '';
      otherContainer.dataset.open = '0';
      // Find the corresponding button and reset its text
      const parentCard = otherContainer.closest('.admin-poll-card');
      if (parentCard) {
        const viewBtn = parentCard.querySelector('.admin-view-btn');
        if (viewBtn) viewBtn.textContent = 'View ▸';
      }
    }
  });

  container.innerHTML = '<div class="admin-votes-loading">Loading...</div>';
  
  // Get poll info to check type
  const poll = state.polls.find(p => p.id === pollId);
  
  if (poll && poll.poll_type === 'text_response') {
    // Handle text responses
    const res = await fetch(`/api/polls/${pollId}/text-responses`);
    const data = await res.json();
    const responses = data.responses || [];
    
    container.innerHTML = '';
    
    if (!responses.length) {
      const emptyMsg = createElement('div', 'admin-votes-empty', '📭 No responses yet for this poll.');
      container.appendChild(emptyMsg);
    } else {
      const header = createElement('div', 'admin-votes-header', [
        createElement('div', 'admin-votes-title', `📝 Text Responses (${responses.length} total)`),
      ]);
      container.appendChild(header);
      
      const responsesList = createElement('div', 'admin-text-responses-list');
      responses.forEach((r) => {
        const responseCard = createElement('div', 'admin-text-response-card');
        const userHeader = createElement('div', 'admin-text-response-user', `👤 ${r.username}`);
        const responseText = createElement('div', 'admin-text-response-text', r.response_text);
        const timestamp = createElement('div', 'admin-text-response-time', new Date(r.created_at).toLocaleString());
        
        responseCard.appendChild(userHeader);
        responseCard.appendChild(responseText);
        responseCard.appendChild(timestamp);
        responsesList.appendChild(responseCard);
      });
      
      container.appendChild(responsesList);
    }
  } else {
    // Handle multiple choice votes
    const data = await apiGetPollVotes(pollId);
    const votes = data.votes || [];

    container.innerHTML = '';

    if (!votes.length) {
      const emptyMsg = createElement('div', 'admin-votes-empty', '📭 No votes yet for this poll.');
      container.appendChild(emptyMsg);
    } else {
      // Create votes header
      const header = createElement('div', 'admin-votes-header', [
        createElement('div', 'admin-votes-title', `📊 Vote Details (${votes.length} total)`),
      ]);
      container.appendChild(header);

      // Group votes by option
      const votesByOption = {};
      votes.forEach((v) => {
        if (!votesByOption[v.optionName]) {
          votesByOption[v.optionName] = [];
        }
        votesByOption[v.optionName].push(v.username);
      });

      // Create vote summary
      const summary = createElement('div', 'admin-votes-summary');
      Object.entries(votesByOption).forEach(([optionName, usernames]) => {
        const optionCard = createElement('div', 'admin-vote-option-card');
        
        const optionHeader = createElement('div', 'admin-vote-option-header', [
          createElement('span', 'admin-vote-option-name', `✓ ${optionName}`),
          createElement('span', 'admin-vote-option-count', `${usernames.length} vote${usernames.length !== 1 ? 's' : ''}`),
        ]);
        
        const userList = createElement('div', 'admin-vote-users');
        usernames.forEach((username) => {
          const userBadge = createElement('span', 'admin-vote-user-badge', username);
          userList.appendChild(userBadge);
        });
        
        optionCard.appendChild(optionHeader);
        optionCard.appendChild(userList);
        summary.appendChild(optionCard);
      });
      
      container.appendChild(summary);

      // Also show chronological list
      const chronoTitle = createElement('div', 'admin-votes-chrono-title', '🕒 Vote History (Chronological)');
      const list = createElement('ul', 'admin-votes-list');
      votes.forEach((v) => {
        const li = createElement('li', 'admin-vote-row', `👤 ${v.username} → ${v.optionName}`);
        list.appendChild(li);
      });
      
      container.appendChild(chronoTitle);
      container.appendChild(list);
    }
  }

  container.dataset.open = '1';
  if (buttonEl) buttonEl.textContent = 'Hide ▾';
}

function renderAdminView() {
  const main = createElement('main', 'polls-main');

  const createBar = createElement('div', 'admin-create-bar');
  const createTitle = createElement('div', 'admin-create-title', 'Polls');
  
  const buttonGroup = createElement('div', 'admin-header-buttons');
  
  const exportAllBtn = createElement('button', 'admin-export-all-btn', '📥 Export All Votes');
  exportAllBtn.type = 'button';
  exportAllBtn.title = 'Export all votes from all polls';
  exportAllBtn.onclick = () => {
    window.location.href = '/api/votes/export';
  };
  
  const exportSummaryBtn = createElement('button', 'admin-export-summary-btn', '📊 Export Summary');
  exportSummaryBtn.type = 'button';
  exportSummaryBtn.title = 'Export polls summary';
  exportSummaryBtn.onclick = () => {
    window.location.href = '/api/polls/export';
  };
  
  const createBtn = createElement('button', 'admin-create-btn', 'Create New Poll');
  
  buttonGroup.appendChild(exportAllBtn);
  buttonGroup.appendChild(exportSummaryBtn);
  buttonGroup.appendChild(createBtn);
  
  const formContainer = createElement('div', 'admin-create-container');
  formContainer.style.display = 'none';

  createBtn.onclick = () => {
    if (!formContainer.firstChild) {
      formContainer.appendChild(renderCreatePollForm());
    }
    formContainer.style.display =
      formContainer.style.display === 'none' || formContainer.style.display === ''
        ? 'block'
        : 'none';
  };

  createBar.appendChild(createTitle);
  createBar.appendChild(buttonGroup);

  const sectionHeader = createElement('div', 'section-header', [
    createElement('div', 'section-title', 'All Polls'),
  ]);

  const grid = createElement('div', 'polls-grid');
  if (!state.polls.length) {
    grid.appendChild(createElement('div', null, 'No polls yet. Create one above.'));
  } else {
    state.polls.forEach((poll) => {
      grid.appendChild(renderPollCard(poll, true));
    });
  }

  main.appendChild(createBar);
  main.appendChild(formContainer);
  main.appendChild(sectionHeader);
  main.appendChild(grid);
  return main;
}

function renderStudentView() {
  const main = createElement('main', 'polls-main');

  if (!currentUsername) {
    const card = createElement('div', 'poll-card poll-card-cyan username-card');

    const headerBg = createElement('div', 'poll-card-header-bg', '42');
    const titleEl = createElement('h3', 'poll-title', 'ENTER_INTRA_USERNAME');
    const descEl = createElement(
      'p',
      'poll-description',
      'Please enter your intra username to start voting. You can only vote once per poll with each username.'
    );
    const headerContent = createElement('div', 'poll-card-header-content', [titleEl, descEl]);
    const header = createElement('div', 'poll-card-header poll-card-header-cyan', [headerBg, headerContent]);

    const form = createElement('form', 'username-form');
    const label = createElement('label', 'username-label', 'INTRA_USERNAME');
    const input = createElement('input', 'username-input');
    input.type = 'text';
    input.required = true;
    input.placeholder = 'login42';

    const footer = createElement('div', 'poll-card-footer poll-card-footer-cyan');
    const submit = createElement('button', 'vote-button vote-button-cyan', '> CONTINUE');
    submit.type = 'submit';

    form.appendChild(label);
    form.appendChild(input);
    footer.appendChild(submit);
    form.appendChild(footer);

    form.onsubmit = (e) => {
      e.preventDefault();
      const v = (input.value || '').trim();
      if (!v) return;
      currentUsername = v;
      localStorage.setItem(USERNAME_KEY, currentUsername);
      render();
    };

    card.appendChild(header);
    card.appendChild(form);

    main.appendChild(card);
    return main;
  }

  const sectionHeader = createElement('div', 'polls-section-header', [
    createElement('div', 'polls-section-title', 'AVAILABLE_POLLS'),
    createElement(
      'div',
      'polls-count',
      (state.polls.length || 0) + ' ACTIVE'
    ),
  ]);

  const grid = createElement('div', 'polls-grid');
  if (!state.polls.length) {
    grid.appendChild(createElement('div', null, 'No polls available yet.'));
  } else {
    state.polls.forEach((poll) => {
      grid.appendChild(renderPollCard(poll, false));
    });
  }

  main.appendChild(sectionHeader);
  main.appendChild(grid);
  return main;
}

function render() {
  appRoot.innerHTML = '';

  // Add 42-style background
  const bg = createElement('div', 'polls-background');
  appRoot.appendChild(bg);

  // Create header for both admin and student
  const headerLeft = createElement('div', 'polls-header-left', [
    createElement('div', 'polls-logo', '42'),
    (function () {
      const wrapper = document.createElement('div');
      wrapper.appendChild(createElement('div', 'polls-header-title', '/ POLLS'));
      wrapper.appendChild(
        createElement(
          'div',
          'polls-header-subtitle',
          ROLE === 'admin' ? 'ADMIN PORTAL' : 'SUBMIT YOUR VOTES'
        )
      );
      return wrapper;
    })(),
  ]);

  const headerRight = createElement('div', 'polls-header-right', [
    createElement('div', null, ROLE === 'admin' ? 'ADMIN_PORTAL' : 'STUDENT_PORTAL'),
    currentUsername ? createElement('div', null, `USER: ${currentUsername}`) : null,
    currentUsername || ROLE === 'admin'
      ? (function () {
          const btn = createElement('button', 'logout-button', 'LOGOUT');
          btn.type = 'button';
          btn.onclick = async () => {
            if (ROLE === 'admin') {
              // Admin logout - call API and redirect
              try {
                await fetch('/api/admin/logout', { method: 'POST' });
                window.location.href = '/login.html';
              } catch (error) {
                console.error('Logout error:', error);
                window.location.href = '/login.html';
              }
            } else {
              // Student logout - clear local storage
              localStorage.removeItem(USERNAME_KEY);
              // clear this user's voted flags
              const prefix = `poll-voted-`;
              Object.keys(localStorage).forEach((k) => {
                if (k.startsWith(prefix) && k.endsWith(`-${currentUsername}`)) {
                  localStorage.removeItem(k);
                }
              });
              currentUsername = '';
              render();
            }
          };
          return btn;
        })()
      : null,
  ]);

  const headerInner = createElement('div', 'polls-header-container', [
    headerLeft,
    headerRight,
  ]);
  const header = createElement('header', 'polls-header', [headerInner]);

  appRoot.appendChild(header);

  if (ROLE === 'admin') {
    appRoot.appendChild(renderAdminView());
  } else {
    appRoot.appendChild(renderStudentView());
  }
}

// Initial load from backend then render
apiGetPolls()
  .then(() => {
    render();
  })
  .catch(() => {
    alert('Failed to load polls from server');
    render();
  });

/*
File:	/tests/shared_chat.js
-----
Script per i messaggi chat NAO-Smart-AI
Condiviso tra test_chat.htm e feedback_dashboard.htm
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Friday, February 27th 2026, 18:30:00 pm
-----
Last Modified: 	February 27th 2026 18:30:00 pm
Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
-----
@license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
Additional Terms under Section 7(b):

The following attribution requirements apply to this work:

1. Copyright notices and author attribution in source code files
   cannot be removed or altered.
2. Any interactive user interface must preserve and display
   author attribution (Copyright, authors, project name).
3. System prompts containing author information cannot be modified
4. Public demonstrations, publications and derivative works
   must credit the original authors.

For full Additional Terms see the LICENSE file.
------------------------------------------------------------------------------
*/

const SharedChatData = {
    movementEmojis: {
        // BodyTalk
        'BodyTalk/Speaking': '💬',
        'BodyTalk/Thinking/Remember': '💭',
        'BodyTalk/Thinking': '💭',

        // Emotions/Negative
        'Emotions/Negative/Angry': '😠',
        'Emotions/Negative/Anxious': '😰',
        'Emotions/Negative/Bored': '😑',
        'Emotions/Negative/Disappointed': '😞',
        'Emotions/Negative/Exhausted': '😫',
        'Emotions/Negative/Fear': '😨',
        'Emotions/Negative/Fearful': '😱',
        'Emotions/Negative/Frustrated': '😤',
        'Emotions/Negative/Humiliated': '😳',
        'Emotions/Negative/Hurt': '😢',
        'Emotions/Negative/Late': '⏰',
        'Emotions/Negative/Sad': '😢',
        'Emotions/Negative/Shocked': '😲',
        'Emotions/Negative/Sorry': '🙏',
        'Emotions/Negative/Surprise': '😮',
        'Emotions/Negative/Surprised': '😮',

        // Emotions/Neutral
        'Emotions/Neutral/Alienated': '🤷',
        'Emotions/Neutral/Annoyed': '😒',
        'Emotions/Neutral/AskForAttention': '👋',
        'Emotions/Neutral/Cautious': '🤨',
        'Emotions/Neutral/Confused': '😕',
        'Emotions/Neutral/Determined': '😤',
        'Emotions/Neutral/Embarrassed': '😅',
        'Emotions/Neutral/Hello': '👋',
        'Emotions/Neutral/Hesitation': '😬',
        'Emotions/Neutral/Innocent': '😇',
        'Emotions/Neutral/Lonely': '😔',
        'Emotions/Neutral/Mischievous': '😏',
        'Emotions/Neutral/Puzzled': '🤔',
        'Emotions/Neutral/Sneeze': '🤧',
        'Emotions/Neutral/Stubborn': '😠',
        'Emotions/Neutral/Suspicious': '🤨',
        'Emotions/Neutral/Thinking': '🤔',

        // Emotions/Positive
        'Emotions/Positive/Amused': '😄',
        'Emotions/Positive/Confident': '😎',
        'Emotions/Positive/Ecstatic': '🤩',
        'Emotions/Positive/Enthusiastic': '🤗',
        'Emotions/Positive/Excited': '😃',
        'Emotions/Positive/Happy': '😊',
        'Emotions/Positive/Hungry': '🍕',
        'Emotions/Positive/Hysterical': '😂',
        'Emotions/Positive/Interested': '🧐',
        'Emotions/Positive/Laugh': '😄',
        'Emotions/Positive/Mocker': '😏',
        'Emotions/Positive/Optimistic': '😊',
        'Emotions/Positive/Peaceful': '😌',
        'Emotions/Positive/Proud': '😌',
        'Emotions/Positive/Relieved': '😅',
        'Emotions/Positive/Shy': '😊',
        'Emotions/Positive/Sure': '👍',
        'Emotions/Positive/Winner': '🏆',

        // Gestures
        'Gestures/Applause': '👏',
        'Gestures/BowShort': '🙇',
        'Gestures/But': '☝️',
        'Gestures/CalmDown': '🤚',
        'Gestures/Caress': '🤗',
        'Gestures/CatchFly': '🦟',
        'Gestures/Choice': '🤷',
        'Gestures/Claw': '✊',
        'Gestures/Coaxing': '🤝',
        'Gestures/ComeOn': '👍',
        'Gestures/CountFive': '5️⃣',
        'Gestures/CountFour': '4️⃣',
        'Gestures/CountMore': '🔢',
        'Gestures/CountOne': '1️⃣',
        'Gestures/CountThree': '3️⃣',
        'Gestures/CountTwo': '2️⃣',
        'Gestures/Desperate': '😩',
        'Gestures/Enthusiastic': '🙌',
        'Gestures/Everything': '🌍',
        'Gestures/Explain': '👨‍🏫',
        'Gestures/Far': '👉',
        'Gestures/Follow': '🚶',
        'Gestures/Freeze': '🧊',
        'Gestures/Give': '🎁',
        'Gestures/Great': '👍',
        'Gestures/HeSays': '💬',
        'Gestures/Hey': '👋',
        'Gestures/Hide': '🙈',
        'Gestures/Hungry': '🍕',
        'Gestures/IDontKnow': '🤷',
        'Gestures/JointHands': '🙏',
        'Gestures/Joy': '😄',
        'Gestures/Kisses': '😘',
        'Gestures/Look': '👀',
        'Gestures/Maybe': '🤔',
        'Gestures/Me': '👤',
        'Gestures/Mime': '🎭',
        'Gestures/Next': '➡️',
        'Gestures/No': '❌',
        'Gestures/Nothing': '🚫',
        'Gestures/OnTheEvening': '🌙',
        'Gestures/Please': '🙏',
        'Gestures/Reject': '🙅',
        'Gestures/Salute': '👋',
        'Gestures/Shoot': '🎯',
        'Gestures/ShowFloor': '⬇️',
        'Gestures/ShowSky': '⬆️',
        'Gestures/Shy': '😊',
        'Gestures/Stretch': '🤸',
        'Gestures/Surprised': '😮',
        'Gestures/Take': '🤲',
        'Gestures/Thinking': '🤔',
        'Gestures/This': '👈',
        'Gestures/WhatSThis': '❓',
        'Gestures/Wings': '🦅',
        'Gestures/Yes': '✅',
        'Gestures/You': '👉',
        'Gestures/YouKnowWhat': '💡',
        'Gestures/Yum': '😋'
    }
};

const SharedChatLogic = {
    getEmojiForMovement: function (movement) {
        for (const [key, emoji] of Object.entries(SharedChatData.movementEmojis)) {
            if (movement.includes(key)) {
                return emoji;
            }
        }
        return '🤖';
    },

    escapeHtml: function (s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    },

    /** FOR test_chat2.htm (Exact original DOM parity) **/
    createMessageDOM: function (text, isUser, movements = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;

        if (movements && movements.length > 0) {
            const movementsDiv = document.createElement('div');
            movementsDiv.className = 'movements-container';
            movements.forEach(mov => {
                const tag = document.createElement('span');
                tag.className = 'movements-tag';
                const emoji = this.getEmojiForMovement(mov);
                const cleanName = mov.replace('animations/Stand/', '');
                tag.textContent = `${emoji} ${cleanName}`;
                movementsDiv.appendChild(tag);
            });
            contentDiv.appendChild(movementsDiv);
        }

        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString('it-IT', {
            hour: '2-digit',
            minute: '2-digit'
        });
        contentDiv.appendChild(timestamp);

        messageDiv.appendChild(contentDiv);
        return messageDiv;
    },

    createActionDOM: function (actionText) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content action-content';

        const badge = document.createElement('div');
        badge.className = 'action-badge-icon';
        badge.textContent = '🎬';
        contentDiv.appendChild(badge);

        contentDiv.innerHTML += `<strong>AZIONE RILEVATA:</strong><br>${this.escapeHtml(actionText)}`;

        const timestamp = document.createElement('div');
        timestamp.className = 'message-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString('it-IT', {
            hour: '2-digit',
            minute: '2-digit'
        });
        contentDiv.appendChild(timestamp);

        messageDiv.appendChild(contentDiv);
        return messageDiv;
    },

    createLoadingDOM: function () {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message bot';
        loadingDiv.id = 'loadingIndicator';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content loading';

        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'loading-dot';
            contentDiv.appendChild(dot);
        }

        loadingDiv.appendChild(contentDiv);
        return loadingDiv;
    },

    /** FOR feedback_dashboard.htm (Includes parsing nested JSON in assistant responses and using dashboard's avatar classes) **/
    renderHistoryEntry: function (entry) {
        const role = (entry.role || entry.type || '').toLowerCase();
        const isUser = role === 'user' || role === 'human';
        const isBot = role === 'assistant' || role === 'bot' || role === 'ai';
        const isSystem = role === 'system';
        const rowClass = isUser ? 'user' : isBot ? 'bot' : isSystem ? 'system' : 'bot';

        const avatar = isUser ? '🧑' : isBot ? '🤖' : isSystem ? '⚙️' : '🤖';
        const label = isUser ? 'Utente' : isBot ? 'NAO' : isSystem ? 'Sistema' : role;

        // Content
        let contentHtml = '';
        let originalContent = entry.content ?? entry.message ?? entry.text ?? '';
        let parsedContentObj = null;

        if (typeof originalContent === 'string') {
            // Attempt to parse if it's stringified JSON from the assistant (like the formatting we saw in logs)
            if (!isUser && originalContent.trim().startsWith('```json')) {
                try {
                    const jsonStr = originalContent.replace(/```json/g, '').replace(/```/g, '').trim();
                    parsedContentObj = JSON.parse(jsonStr);
                } catch (e) { }
            } else if (!isUser && originalContent.trim().startsWith('{')) {
                try {
                    parsedContentObj = JSON.parse(originalContent.trim());
                } catch (e) { }
            } else {
                contentHtml = this.escapeHtml(originalContent);
            }
        }

        // Chunks logic mapped
        let chunksHtml = '';
        let chunksArr = null;

        if (parsedContentObj && parsedContentObj.chunks) {
            chunksArr = parsedContentObj.chunks;
        } else if (entry.chunks && Array.isArray(entry.chunks)) {
            chunksArr = entry.chunks;
        }

        if (chunksArr && Array.isArray(chunksArr)) {
            chunksHtml = chunksArr.map(chunk => {
                let mv = '';
                if (chunk.movements && chunk.movements.length > 0) {
                    mv = `<div class="movements-wrap">` +
                        chunk.movements.map(m => {
                            const shortName = m.replace('animations/Stand/', '');
                            return `<span class="mv-tag">${this.getEmojiForMovement(m)} ${this.escapeHtml(shortName)}</span>`;
                        }).join('') +
                        `</div>`;
                }
                return `<div style="margin-bottom:6px;">${this.escapeHtml(chunk.text || '')}${mv}</div>`;
            }).join('');
        }

        // Se è fallback su parsed content ma senza chunk
        if (!chunksHtml && parsedContentObj && parsedContentObj.response && typeof parsedContentObj.response === 'string') {
            contentHtml = this.escapeHtml(parsedContentObj.response);
        } else if (!chunksHtml && originalContent && typeof originalContent === 'string' && !contentHtml) {
            contentHtml = this.escapeHtml(originalContent);
        }

        let movementsHtml = '';
        if (entry.movements && entry.movements.length > 0) {
            movementsHtml = `<div class="movements-wrap">` +
                entry.movements.map(mv => {
                    const emoji = this.getEmojiForMovement(mv);
                    const shortName = mv.replace('animations/Stand/', '');
                    return `<span class="mv-tag">${emoji} ${this.escapeHtml(shortName)}</span>`;
                }).join('') + `</div>`;
        }

        // Action line
        let actionHtml = '';
        let actionExtracted = entry.action || (parsedContentObj ? parsedContentObj.action : null);
        if (actionExtracted && actionExtracted !== 'NO_ACTION') {
            actionHtml = `<div class="msg-row action" style="margin-top:4px;">
            <div class="msg-avatar">🎬</div>
            <div class="msg-bubble-wrap">
                <div class="msg-label">Azione NAO</div>
                <div class="msg-bubble">${this.escapeHtml(actionExtracted)}</div>
            </div>
        </div>`;
        }

        // Timestamp
        let ts = '';
        if (entry.timestamp || entry.created_at || entry.time) {
            try {
                const d = new Date(entry.timestamp || entry.created_at || entry.time);
                ts = d.toLocaleString('it-IT', { dateStyle: 'short', timeStyle: 'short' });
            } catch (_) { }
        }

        const body = contentHtml || chunksHtml || (typeof originalContent === 'string' ? this.escapeHtml(originalContent) : JSON.stringify(originalContent));

        return `
        <div class="msg-row ${rowClass}">
            <div class="msg-avatar">${avatar}</div>
            <div class="msg-bubble-wrap">
                <div class="msg-label">${label}${ts ? ' · ' + ts : ''}</div>
                <div class="msg-bubble">${body}${movementsHtml}</div>
            </div>
        </div>${actionHtml}`;
    }
};

$(document).ready(function() {
    // Handle file upload
    $('#upload-form').on('submit', function(e) {
        e.preventDefault();
        
        var fileInput = $('#document-upload')[0];
        if (fileInput.files.length === 0) {
            showUploadStatus('Please select a PDF file', 'error');
            return;
        }
        
        var file = fileInput.files[0];
        if (!file.name.endsWith('.pdf')) {
            showUploadStatus('Only PDF files are supported', 'error');
            return;
        }
        
        // Create FormData object
        var formData = new FormData();
        formData.append('document', file);
        
        // Show processing status
        showUploadStatus('Processing file...', '');
        
        // Send AJAX request
        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                showUploadStatus('File processed successfully! You can now ask questions.', 'success');
            },
            error: function(xhr) {
                let errorMsg = 'Error processing file';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                showUploadStatus(errorMsg, 'error');
            }
        });
    });
    
    // Handle query submission
    $('#submit-query').on('click', function() {
        submitQuery();
    });
    
    // Handle Enter key press in query input
    $('#query-input').on('keypress', function(e) {
        if (e.which === 13) {
            submitQuery();
        }
    });
    
    // Function to submit query
    function submitQuery() {
        var query = $('#query-input').val().trim();
        if (!query) return;
        
        // Add user message to chat
        addMessage(query, 'user');
        
        // Clear input
        $('#query-input').val('');
        
        // Show thinking indicator
        addThinkingIndicator();
        
        // Send query to server
        $.ajax({
            url: '/query',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ query: query }),
            success: function(response) {
                // Remove thinking indicator
                removeThinkingIndicator();
                
                // Add bot response to chat
                addMessage(response.bot_response, 'bot');
                
                // Scroll to bottom of chat
                scrollChatToBottom();
            },
            error: function(xhr) {
                // Remove thinking indicator
                removeThinkingIndicator();
                
                let errorMsg = 'Error processing your question';
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    errorMsg = xhr.responseJSON.error;
                }
                
                // Add error message
                addMessage(errorMsg, 'bot error');
                
                // Scroll to bottom of chat
                scrollChatToBottom();
            }
        });
    }
    
    // Function to add message to chat
    function addMessage(message, type) {
        var avatar = '';
        
        if (type === 'user') {
            avatar = '<img src="https://i.ibb.co/d2vRb5B/vecteezy-medical-student-icon-6397840.jpg" alt="User">';
        } else {
            avatar = '<img src="https://i.ibb.co/RDR6q2g/medical-robot.png" alt="Assistant">';
        }
        
        var messageHtml = `
            <div class="chat-message ${type}">
                <div class="avatar">
                    ${avatar}
                </div>
                <div class="message">
                    ${message}
                </div>
            </div>
        `;
        
        $('#chat-messages').append(messageHtml);
        scrollChatToBottom();
    }
    
    // Add thinking indicator
    function addThinkingIndicator() {
        var indicatorHtml = `
            <div class="chat-message bot" id="thinking-indicator">
                <div class="avatar">
                    <img src="https://i.ibb.co/RDR6q2g/medical-robot.png" alt="Assistant">
                </div>
                <div class="message">
                    <div class="thinking-dots">
                        <span>.</span><span>.</span><span>.</span>
                    </div>
                </div>
            </div>
        `;
        
        $('#chat-messages').append(indicatorHtml);
        scrollChatToBottom();
    }
    
    // Remove thinking indicator
    function removeThinkingIndicator() {
        $('#thinking-indicator').remove();
    }
    
    // Scroll chat to bottom
    function scrollChatToBottom() {
        var chatMessages = $('#chat-messages');
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }
    
    // Function to show upload status
    function showUploadStatus(message, type) {
        var statusElement = $('#upload-status');
        statusElement.removeClass('success error').addClass(type);
        statusElement.text(message);
    }
});
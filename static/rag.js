// RAG functionality for AI-powered answers
function performRagQuery() {
    const query = document.getElementById('rag-query').value;
    const provider = document.querySelector('input[name="provider"]:checked').value;
    const temperature = document.getElementById('temperature').value;
    
    if (!query) {
        alert('Please enter a question');
        return false;
    }
    
    const resultsDiv = document.getElementById('rag-results');
    resultsDiv.innerHTML = '<p>Generating AI response...</p>';
    
    // Call the RAG API
    fetch(`/api/rag?q=${encodeURIComponent(query)}&provider=${provider}&temperature=${temperature}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = `
                    <div class="error-message">
                        <p><strong>Error:</strong> ${data.error}</p>
                    </div>
                `;
                return;
            }
            
            // Format the answer with markdown
            let formattedAnswer = data.answer;
            
            // Format the sources
            let sourcesHtml = '';
            if (data.sources && data.sources.length > 0) {
                sourcesHtml = '<h3>Sources</h3><div class="sources-list">';
                data.sources.forEach((source, index) => {
                    sourcesHtml += `
                        <div class="source-item">
                            <p><strong>${index+1}. ${source.title}</strong></p>
                            <p>Timestamp: ${source.timestamp}</p>
                            <p><a href="${source.url}" target="_blank">Watch Video at This Timestamp</a></p>
                        </div>
                    `;
                });
                sourcesHtml += '</div>';
            }
            
            resultsDiv.innerHTML = `
                <div class="rag-answer">
                    <h3>AI-Generated Answer</h3>
                    <div class="answer-content">${formattedAnswer.replace(/\n/g, '<br>')}</div>
                </div>
                ${sourcesHtml}
            `;
        })
        .catch(error => {
            console.error('Error:', error);
            resultsDiv.innerHTML = 
                '<p>An error occurred while generating the answer. Please try again later.</p>';
        });
    
    return false;
} 
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsContainer = document.getElementById('results-container');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value.trim();
        if (!query) return;

        resultsContainer.innerHTML = '<p>Searching...</p>';

        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            resultsContainer.innerHTML = '<p>Error: Could not perform search.</p>';
            console.error('Search error:', error);
        });
    }

    function displayResults(results) {
        if (!results || results.length === 0) {
            resultsContainer.innerHTML = '<p>No results found.</p>';
            return;
        }

        resultsContainer.innerHTML = '';
        results.forEach(result => {
            const resultElement = document.createElement('div');
            resultElement.className = 'result-item';
            
            const timestamp = result.timestamp ? formatTimestamp(result.timestamp) : '';
            const videoUrl = result.video_url ? `${result.video_url}&t=${Math.floor(result.timestamp)}` : '#';
            
            resultElement.innerHTML = `
                <h3 class="result-title">${result.title || 'Untitled'}</h3>
                <p>${result.text || ''}</p>
                <p><strong>Relevant timestamp:</strong> ${timestamp}</p>
                <a class="result-link" href="${videoUrl}" target="_blank">Watch Video at Timestamp</a>
            `;
            
            resultsContainer.appendChild(resultElement);
        });
    }

    function formatTimestamp(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}); 
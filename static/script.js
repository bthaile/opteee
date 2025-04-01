document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const searchType = document.getElementById('search-type');
    const textResultsContainer = document.getElementById('text-results');
    const videoResultsContainer = document.getElementById('video-results');

    searchButton.addEventListener('click', performSearch);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });

    function performSearch() {
        const query = searchInput.value.trim();
        if (!query) return;

        // Clear previous results
        textResultsContainer.innerHTML = '<p>Searching...</p>';
        videoResultsContainer.innerHTML = '';

        // Get the search type
        const type = searchType.value;

        fetch(`/api/search?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            textResultsContainer.innerHTML = '<p>Error: Could not perform search.</p>';
            console.error('Search error:', error);
        });
    }

    function displayResults(data) {
        const results = data.results || [];
        
        if (results.length === 0) {
            textResultsContainer.innerHTML = '<p>No results found.</p>';
            videoResultsContainer.innerHTML = '';
            return;
        }

        // Clear containers
        textResultsContainer.innerHTML = '';
        videoResultsContainer.innerHTML = '';

        // Process results
        results.forEach(result => {
            // Display text result
            const textResultElement = createTextResult(result);
            textResultsContainer.appendChild(textResultElement);
            
            // Display video result (if there's a video URL)
            if (result.video_url) {
                const videoResultElement = createVideoResult(result);
                videoResultsContainer.appendChild(videoResultElement);
            }
        });
    }

    function createTextResult(result) {
        const resultElement = document.createElement('div');
        resultElement.className = 'result-item';
        
        resultElement.innerHTML = `
            <h3 class="result-title">${result.title || 'Untitled'}</h3>
            <p>${result.content || ''}</p>
            <p><strong>Relevance Score:</strong> ${result.score ? (result.score * 100).toFixed(1) + '%' : 'N/A'}</p>
        `;
        
        return resultElement;
    }

    function createVideoResult(result) {
        const resultElement = document.createElement('div');
        resultElement.className = 'result-item video-result';
        
        const timestamp = result.timestamp ? formatTimestamp(result.timestamp) : '';
        const videoUrl = result.video_url || '#';
        const duration = result.duration || '';
        
        resultElement.innerHTML = `
            <div class="video-thumbnail">
                <span>▶</span>
            </div>
            <div class="video-info">
                <div class="video-title">${result.title || 'Untitled'}</div>
                <br>
                <div class="video-metadata">
                    <a class="result-link" href="${videoUrl}" target="_blank">Watch Video</a> | 
                    Timestamp: ${timestamp} ${duration ? `| Duration: ${duration}` : ''}
                </div>
                <br>
                <div class="video-content">${result.content || ''}</div>
            </div>
        `;
        
        return resultElement;
    }

    function formatTimestamp(seconds) {
        if (typeof seconds === 'string' && seconds.includes(':')) {
            return seconds; // Already formatted
        }
        
        seconds = parseInt(seconds);
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}); 
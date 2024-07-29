const subtitles = [];
// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');
    
tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'JDjZTYQX2xY',
    playerVars: {
      'playsinline': 1
    },
    events: {
      'onReady': onPlayerReady,
    }
  });
}

// Function to load subtitles from the JSON file
function loadSubtitles() {
    fetch('/static/1.json') // Path to your subtitles JSON file
      .then(response => response.json())
      .then(data => {
        subtitles.push(...data); // Add subtitle data to the array
      })
      .catch(error => console.error('Error loading subtitles:', error));
  }


  // Function to update subtitles based on video time
function updateSubtitles() {
    const currentTime = player.getCurrentTime();
    const subtitleDiv = document.getElementById('subtitles');
    
    // Clear existing subtitles
    subtitleDiv.innerHTML = '';
  
    // Find and display the current subtitle based on video time
    subtitles.forEach(subtitle => {
      if (currentTime >= subtitle.start && currentTime < (subtitle.start + subtitle.duration)) {
        subtitleDiv.innerHTML = subtitle.text;
      }
    });
  }

function onPlayerReady(event) {
    loadSubtitles(); // Load subtitles when player is ready
    // Update subtitles every 500 milliseconds
    setInterval(updateSubtitles, 500);
  }


  
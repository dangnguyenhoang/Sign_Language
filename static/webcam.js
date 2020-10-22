
Webcam.set({
  width: 640,
  height:480,
  image_format: 'jpeg',
  jpeg_quality:90
});

Webcam.attach('#sketch-holder');

function startTraining(){
  let starting_btn = document.getElementsByClassName("starting_training_btn")[0];
  starting_btn.style.display = "none";
  let stopping_btn = document.getElementsByClassName("stopping_training_btn")[0];
  stopping_btn.style.display = "block";
  setTimeout(function(){
    interval = setInterval(sendData, 1000);
  }, 1000); 
}

function stopTraining(){  
  let starting_btn = document.getElementsByClassName("starting_training_btn")[0];
  starting_btn.style.display = "block";
  let stopping_btn = document.getElementsByClassName("stopping_training_btn")[0];
  stopping_btn.style.display = "none";
  clearInterval(interval);
}

function sendData() {
  Webcam.snap(function(data_uri){


      let json_data = {'data-uri': data_uri}
      fetch('/predict/', {
        method: 'POST',
        processData: false,
        headers: {
          'Accept': 'application/json, text/plain, */*',
          'Content-Type': 'application/json; charset=utf-8'
        },
        body: JSON.stringify(json_data)
      }).then(res=>res.json())
      .then(res => {
        console.log(res);
        // document.getElementById("cond1").innerHTML = res.cond1;
        document.getElementById("feedback").value = document.getElementById("feedback").value + res['word'];
        
        })
    })
  }

function saveData() {
  let json_data = {'type-exercise': type_exercise,
                    'count':count_to_db}
  fetch('/saveData/', {
    method: 'POST',
    processData: false,
    headers: {
      'Accept': 'application/json, text/plain, */*',
      'Content-Type': 'application/json; charset=utf-8'
    },
    body: JSON.stringify(json_data)
  }).then(res=>res.json())
}

function modelReady() {
  console.log('Model Loaded');
}

function draw() {
  background(200)
  image(video, 0, 0, width, height);

  // We can call both functions to draw all keypoints and the skeletons
  drawKeypoints();
  drawSkeleton();
}

// A function to draw ellipses over the detected keypoints
function drawKeypoints()  {
  // Loop through all the poses detected
  if (poses.length > 0){
    for (let i = 0; i < poses.length; i++) {
      // For each pose detected, loop through all the keypoints
      let pose = poses[i].pose;
      for (let j = 5; j < pose.keypoints.length; j++) {
        // A keypoint is an object describing a body part (like rightArm or leftShoulder)
        let keypoint = pose.keypoints[j];
        // Only draw an ellipse is the pose probability is bigger than 0.6
        if (keypoint.score > 0.5) {
          fill(250,182,23);
          stroke(20);
          strokeWeight(2);
          ellipse(keypoint.position.x, keypoint.position.y, 12, 12);
        }
      }
    }
  }
}

// A function to draw the skeletons
function drawSkeleton() {
  // Loop through all the skeletons detected
  if (poses.length > 0){
    for (let i = 0; i < poses.length; i++) {
      let skeleton = poses[i].skeleton;
      // For every skeleton, loop through all body connections
      for (let j = 0; j < skeleton.length; j++) {
        if (![0,5,10,11].includes(j)){
        let partA = skeleton[j][0];
        let partB = skeleton[j][1];
        stroke(255);
        strokeWeight(2);
        line(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
        }
      }
    }
  }
}





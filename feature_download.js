// Create a button and append it to the page
var button = document.createElement("button");
button.innerHTML = "Download";
button.style.position = "fixed";
button.style.bottom = "60px";
button.style.right = "60px";
button.style.width = "200px";
button.style.height = "40px";
button.style.zIndex = "9999";

button.style.backgroundColor = "rgba(0,86,210,1)";
button.style.color = "white";
button.style.fontSize = "20px";
button.style.fontWeight = "bold";
button.style.fontFamily = "system-ui";
button.style.borderRadius = "10px";
document.body.appendChild(button);

// Function to crawl questions and answers and save them into a text file
function crawlQuestionsAndAnswers() {
  try{
  // Check in the right page if not: crash whole system 
  var check_point = document.querySelector('.css-k008qs').innerText;
  
  // Title of course
  var title = document.querySelector('.rc-TunnelVisionHeader').innerText;
  // Code to crawl questions and answers here
  var questions_answers = document.querySelectorAll(".rc-FormPartsQuestion"); // Adjust the selector based on the structure of the Coursera page

  // Loop through all questions
  var data = [];
  for (var i = 0; i < questions_answers.length; i++) {
    var point = questions_answers[i].querySelector('.rc-FormPartsQuestion__pointsCell').innerText 
    if (point == '1 / 1 point'){

      var question = questions_answers[i].querySelector('.rc-FormPartsQuestion__contentCell').innerText;
      var answers = questions_answers[i].querySelectorAll('.rc-Option.rc-Option--isReadOnly')
      var corrects = questions_answers[i].querySelectorAll('.cui-isChecked')
      temp_data = {}
      temp_data['Question'] = question
      temp_data['Answer'] = []
      temp_data['Correct'] = []
      temp_data['Title'] = title
      
      //answers
      for (var j = 0; j < answers.length; j++) {
        temp_data['Answer'].push(answers[j].innerText)
      }
      //corrects
      for (var j = 0; j < corrects.length; j++) {
        temp_data['Correct'].push(corrects[j].innerText)
      }
      //push to final data
      data.push(temp_data)
   }
  }

  // create file name
  const currentDate = new Date();
  const formattedTime = `${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${currentDate.getDate().toString().padStart(2, '0')}-${currentDate.getHours().toString().padStart(2, '0')}h-${currentDate.getMinutes().toString().padStart(2, '0')}m-${currentDate.getSeconds().toString().padStart(2, '0')}s.json`;
  
  // create download object
  const dataString = JSON.stringify(data, null, 2);
  var blob = new Blob([dataString], { type: "application/json" });
  var url = URL.createObjectURL(blob);

  // Create a download link and click it to initiate the download
  var a = document.createElement("a");
  a.href = url;
  a.download = formattedTime;
  a.click();
  alert('Download Complete!!!')
  }

 catch{alert('Wrong page to download !!!')}

}

// Add click event listener to the button
button.addEventListener("click", crawlQuestionsAndAnswers);

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
  // Check in the right page
  var check_point = document.querySelector('.css-k008qs').innerText;
  

  // Title of course
  var title = document.querySelector('.rc-TunnelVisionHeader').innerText;
  // Code to crawl questions and answers here
  var questions_answers = document.querySelectorAll(".rc-FormPartsQuestion"); // Adjust the selector based on the structure of the Coursera page

  var data = "";
  for (var i = 0; i < questions_answers.length; i++) {
    var point = questions_answers[i].querySelector('.rc-FormPartsQuestion__pointsCell').innerText
    
    if (point == '1 / 1 point'){

      var question = questions_answers[i].querySelector('.rc-FormPartsQuestion__contentCell').innerText;
      var answers = questions_answers[i].querySelectorAll('.rc-Option.rc-Option--isReadOnly')
      var corrects = questions_answers[i].querySelectorAll('.cui-isChecked')

      //seperate question
      if (i!== 0){
        data += '@@@'
      }
      data += title + '|||'

      //question
      data += question + "|||"

      //answers
      for (var j = 0; j < answers.length; j++) {
          if (j!== 0){
              data += '^^^'
          }
          data += answers[j].innerText 
      }
      data += "|||"

      //corrects
      for (var j = 0; j < corrects.length; j++) {
          if (j!== 0){
              data += '^^^'
          }
          data += corrects[j].innerText 
      }

   }
  }
  
  var blob = new Blob([data], { type: "text/plain" });
  var url = URL.createObjectURL(blob);

  // Create a download link and click it to initiate the download
  var a = document.createElement("a");
  a.href = url;
  a.download = "coursera_questions_answers.txt";
  a.click();
  alert('Download Complete!!!')
  }

 catch{alert('Wrong page to download !!!')}

}

// Add click event listener to the button
button.addEventListener("click", crawlQuestionsAndAnswers);

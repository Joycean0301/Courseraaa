// Create a button and append it to the page
var button = document.createElement("button");
button.innerHTML = "Fill answer";
button.style.position = "fixed";
button.style.bottom = "120px";
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
function fillQuestionsAndAnswers() {
  // URL file Json
  const url = chrome.runtime.getURL('json_folder/02-06-2023-22h-37p-53s.json');
  // Gets questions and answers here
  const question_answers = document.querySelectorAll(".rc-FormPartsQuestion"); // Adjust the selector based on the structure of the Coursera page

  // Pass each block of QA
  for (var i = 0; i < question_answers.length; i++) {
    // Define QA
    const question = question_answers[i].querySelector('.rc-FormPartsQuestion__contentCell').innerText;
    const answers = question_answers[i].querySelectorAll('label._1oyudm1w');
    
    // Check quesion in the database if match -> Get the correct answer
    fetch(url).then((response) => response.json()).then((json) => {
      for (let z = 0; z < json.length; z++) {
        const item = json[z];
        if (item.Question == question){
          const full_correct_answer = item.Correct;
        
          // Pass all answer if it correct -> Click
          for (var j = 0; j < answers.length; j++) {
            if (full_correct_answer.includes(answers[j].innerText)){
              answers[j].click();
       }
      }
     }
    }
   }
  )
 }
}

// Add click event listener to the button
button.addEventListener("click", fillQuestionsAndAnswers);





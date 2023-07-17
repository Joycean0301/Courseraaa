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
  const url = chrome.runtime.getURL('json_folder/AIH301m.json');

  // Gets questions and answers here
  const question_answers = document.querySelectorAll(".rc-FormPartsQuestion"); // Adjust the selector based on the structure of the Coursera page

  // Pass each block of QA
  for (var i = 0; i < question_answers.length; i++) {
    // Define QA
    const question = question_answers[i].querySelector('.rc-FormPartsQuestion__contentCell').innerText;
    const answers = question_answers[i].querySelectorAll('label._1oyudm1w');
    
    // create answer_check_1
    var check_answers = ''
    let list_answer_web = []
    for (var k = 0; k < answers.length; k++) {
      check_answers += answers[k].innerText;
      list_answer_web.push(answers[k].innerText)}
    // answer_check_sort
    const characters = check_answers.split('');
    const sortedCharacters = characters.sort();
    const sortedWord = sortedCharacters.join('');
    

    // Check quesion in the database if match -> Get the correct answer
    fetch(url).then((response) => response.json()).then((json) => {
      for (var z = 0; z < json.length; z++) {
        const item = json[z];
        
        if (question == item.Question){
          
          // create answer_check_2
          var checkanswertwo = ''
          for (var l = 0; l < item.Answer.length; l++) {
            checkanswertwo += item.Answer[l]}
          // answer2 check sort
          const characterstwo = checkanswertwo.split('')
          const sortedCharacterstwo = characterstwo.sort();
          const sortedWordtwo = sortedCharacterstwo.join('');


          // check answers match answers in database
          if (sortedWordtwo == sortedWord){
            const full_correct_answer = item.Correct;
            
            // Pass all answer if it correct -> Click
            for (var j = 0; j < full_correct_answer.length; j++) {
              for (var n = 0; n < list_answer_web.length; n++)   {
                if (full_correct_answer[j]==list_answer_web[n])  {
                  answers[n].click();

         }
        }
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










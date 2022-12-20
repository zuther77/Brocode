const outputResponse = document.getElementById('outputTextArea')
const textarea = document.querySelector('textarea')
let lang = document.getElementById('language')
let theme = document.getElementById('changeTheme')
let font = document.getElementById('fontSize')
const lineNumbers = document.querySelector('.line-numbers')
let output_text = document.getElementById('output_box')
let run_button = document.getElementById('run-button')

run_button.addEventListener('click', executeCode)



// defaul ace editor settings 
var editor = ace.edit("editor");
editor.setTheme("ace/theme/cobalt");
editor.session.setMode("ace/mode/c_cpp");
editor.session.setUseWrapMode(true);
document.getElementById('editor').style.fontSize = '15px';





function changeLanguage() {
  langData = lang.options[lang.selectedIndex].value
  if (langData == "c" || langData == "cpp") editor.session.setMode("ace/mode/c_cpp");
  else if (langData == "cs") editor.session.setMode("ace/mode/csharp");
  else if (langData == "java") editor.session.setMode("ace/mode/java");
  else if (langData == "py") editor.session.setMode("ace/mode/python");
  else if (langData == "go") editor.session.setMode("ace/mode/golang");
  else if (langData == "js") editor.session.setMode("ace/mode/javascript");

}

function changeTheme() {
  let themeType = theme.options[theme.selectedIndex].value
  if (themeType == "ambiance") editor.setTheme("ace/theme/ambiance");
  else if (themeType == "chaos") editor.setTheme("ace/theme/chaos");
  else if (themeType == "chrome") editor.setTheme("ace/theme/chrome");
  else if (themeType == "cobalt") editor.setTheme("ace/theme/cobalt");
  else if (themeType == "dracula") editor.setTheme("ace/theme/dracula");
  else if (themeType == "eclipse") editor.setTheme("ace/theme/eclipse");
  else if (themeType == "github") editor.setTheme("ace/theme/github");
  else if (themeType == "twilight") editor.setTheme("ace/theme/twilight");
  else if (themeType == "xcode") editor.setTheme("ace/theme/xcode");
  else if (themeType == "sqlserver") editor.setTheme("ace/theme/sqlserver");
}

function changeFontSize() {
  let fontValue = font.options[font.selectedIndex].value
  if (fontValue == "9") document.getElementById('editor').style.fontSize = '9px';
  if (fontValue == "10") document.getElementById('editor').style.fontSize = '10px';
  if (fontValue == "15") document.getElementById('editor').style.fontSize = '15px';
  if (fontValue == "18") document.getElementById('editor').style.fontSize = '18px';
  if (fontValue == "22") document.getElementById('editor').style.fontSize = '22px';
  if (fontValue == "25") document.getElementById('editor').style.fontSize = '25px';
}


let clear_button = document.getElementById('clear-button')
clear_button.addEventListener('click', () => {
  // console.log(output_text.value);
  output_text.value = ''
})



var codeData, langData, inputData
const inputTextAreaContent = document.getElementById('input')

function getall() {
  codeData = editor.getSession().getValue()
  langData = lang.options[lang.selectedIndex].value
  console.log(codeData);
}






// var result
// async function runCode() {
//   async function postData() {
//     const req = await fetch("https://cod-ey-api.vercel.app/", {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({
//         code: codeData,
//         language: langData,
//         input: inputData
//       })
//     })
//   }
//   async function getData() {
//     const res = await fetch("https://cod-ey-api.vercel.app/getOutput", {
//       method: 'GET',
//     })
//     result = await res.json()
//     outputResponse.value = result.getOutput
//   }

//   let promise = new Promise((resolve, reject) => {
//     resolve(getInputData())
//   })
//   promise.then(postData()).then(getData())

// }

function executeCode() {
  getall()
}

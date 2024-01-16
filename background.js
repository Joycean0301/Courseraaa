chrome.action.onClicked.addListener(function (tab) {
    chrome.scripting.executeScript(tab.id, { file: "feature_download.js" });
  });

chrome.action.onClicked.addListener(function (tab) {
    chrome.scripting.executeScript(tab.id, { file: "feature_fill.js" });
  });
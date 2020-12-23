
// Dynamic date change in all footers
var date = new Date();
var year = date.getFullYear();
document.getElementById("footer").innerHTML = '&copy; Copyright ' + year + ' Ivonaku';

// Search for languages on wiki with added 'language' value to the search input
var myform = document.getElementById("languageSearch");
myform.onsubmit = function(){
    var searchValue = document.getElementById('inputLanguage').value;

    if (searchValue.includes("language") === true) {
        myform.submit();
    }
    else {
        document.getElementById('inputLanguage').value = document.getElementById('inputLanguage').value + ' language';
        myform.submit();
    }
};

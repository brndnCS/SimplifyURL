function customURLForm()
{
    document.getElementById("customURLFormContainer").style.display = "block";
}


function copyToClipboardRandom()
{
    var text = document.getElementById("idSimplifiedURL").getAttribute("href");
    navigator.clipboard.writeText(text);
}

function copyToClipboardCustom()
{
    var text = document.getElementById("idCustomURL").getAttribute("href");
    navigator.clipboard.writeText(text)
}
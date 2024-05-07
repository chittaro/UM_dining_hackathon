let menuItems = document.querySelectorAll(".menuItemDiv");

for (let i = 0; i < menuItems.length; i++){
    menuItems[i].addEventListener("click", function(){
        console.log("pressed");
        this.classList.toggle("active");
        let factBox = this.nextElementSibling;
        if (factBox.style.maxHeight){
            factBox.style.maxHeight = null;
        }
        else {
            factBox.style.maxHeight = factBox.scrollHeight + "px";
        }
    });
}
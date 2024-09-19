

$(document).ready(function() {
    $(".hidebox p").hide();
    $(".hidebox h4").css("background-color", "#0066FF");
});


$(".hidebox h4").click(function () {
    $(this).next("p").show("slow");
    $(this).css("background-color", "#e7e7e7");
    
});


$(".menu_list a").mouseenter(function () {
    $(this).addClass("active"); }).mouseleave(function () {
    $(this).removeClass("active"); });
    
$(".important img").hover(
    function() {
    $(this).animate({
    width: "300px",
    height: "165px",
    borderRadius: "2%"
    }, "slow");
    }, function() {
    $(this).animate({
    width: "270px",
    height: "150px",
    borderRadius: "10%"
    }, "slow");
});

// const callback = () => {
//     alert("Вы отправили заявку, ожидайте нашего звонка!");
//     };
// const button = document.querySelector('.form_btn');

// button.addEventListener('click', callback);


var elem = document.getElementById('nav');
    elem.onmouseover = function () {
        elem.style.opacity = "0.4";
    };
    elem.onmouseleave = function () {
        elem.style.opacity = "1";
    }






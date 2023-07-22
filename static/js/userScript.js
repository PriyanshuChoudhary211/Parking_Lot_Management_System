const squares = document.querySelectorAll(".square");

const gradientColors = [
  "whitesmoke",
  "#e9e9e9",
  "#e6e6e6",
  "white",
  "white",
  "white",
  "#e6e6e6",
  "#e9e9e9",
  "whitesmoke",
];
squares.forEach((square, index) => {
    square.style.backgroundColor = gradientColors[index];
    square.style.animationDelay = `${index * 0.125}s`;
});
setInterval(function() {   
    $(".spinnerLoading").css('display','none');
    console.log('loding');        
  }, 3000);

// $('#userBooking').css('display','none');
// function checkStatus()
// {
//     $('#userBooking').css('display','block');
//     $('#userBookStatus').css('display','none');
// }



function payAndBookSlot(){
    var pop=document.getElementById('popupActionThree');
    var blur=document.getElementById('blur');
        pop.classList.toggle('active');
        blur.classList.toggle('active');
        $('#userBooking').css('display','none');   

        // pop.classList.toggle('active');

}
function payAndBookSlotTwo()
{
    var pop=document.getElementById('popupActionThree');
    var blur=document.getElementById('blur');
        pop.classList.toggle('active');
        blur.classList.toggle('active');
    $('#userBooking').css('display','none');   
}

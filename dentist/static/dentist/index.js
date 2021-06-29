document.addEventListener('DOMContentLoaded', function(){

    const add_med_list = document.querySelector('.add_med_list');
    add_med_list.style.display = "none";

    const show_hide_btn = document.getElementById('add__treatbtn');
    show_hide_btn.onclick = function(){
    console.log("rer");

     if(add_med_list.style.display === "none"){
         add_med_list.style.display = "block";
     }
     else{
         add_med_list.style.display = 'none';
     }

}   
  
});



 

    

document.addEventListener('DOMContentLoaded', function(){
   selectdate();
   document.querySelector('.appointment-form').style.display = 'none';
   document.querySelector('#add-appointment').addEventListener('click', ()=>{
       if(document.querySelector('.appointment-form').style.display === 'block'){
           document.querySelector('.appointment-form').style.display = 'none';
       }
        else{
            document.querySelector('.appointment-form').style.display = 'block';

           }
       }
       );
       
   }) 

function selectdate(){
    $('#datepicker').datetimepicker()
}

    

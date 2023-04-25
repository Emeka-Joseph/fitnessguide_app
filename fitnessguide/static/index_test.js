//Text file data

$(document).ready(function(){
    function load_data(query){
         $.ajax({
            url: "/ajaxlivesearch",
            method:"POST",
            data:{query:query},
            success:function(data){
                $('#result').html(data);
            }
    })

    }

    $('#focus-trial').keyup(function(){
        var search = $(this).val();
        if(search!=''){
            load_data(search);
        }else{
            load_data();
        }
    })
})

let textButton = document.querySelector("#text-btn");

textButton.addEventListener('click', function(){
     //alert('I am clicked')

    // Create an AJAX Request
    let xhr = new XMLHttpRequest();

    // Then prepare the Request (to tell which file you would want to work on and what operation are you expecting)

    xhr.open('GET' , 'static/data/message.txt',  true);
    //Send the Request

    xhr.send();
    //Process the Request

    xhr.onload = () => {
        if(xhr.status === 200){
            let data = xhr.responseText;
            dtd(data)
        };
    };
});

// display TextData

let dtd = (data) => {
    let ht = `<p> ${data} </p>`;
    document.querySelector('#text-card').innerHTML=ht;
};

// JSON button
let jsonButton = document.querySelector('#json-btn')
jsonButton.addEventListener('click', function(){

    let xhr = new XMLHttpRequest();
    xhr.open('GET', 'static/data/mobile.json', true)

    xhr.send();

    xhr.onload = () =>{
        if(xhr.status === 200){
            let data = xhr.responseText
            // convert the object type 
            let mobile = JSON.parse(data)
            displayjson(mobile)
        };
    };
});

// Display the JSON Data

/* let dtd = (data) => {
    let ht = `<p> ${data} </p>`;
    document.querySelector('#text-card').innerHTML=ht;
};*/

let displayjson = (mobile) =>{
    let jsont = ` 
        <table class="table table-striped">
            <thead> 
                <tr>
                    <th> S/N</th>
                    <th> Items </th>
                    <th> Values </th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td> ID </td>
                    <td> ${mobile.id} </td>
                </tr>
                <tr>
                    <td>2</td>
                    <td> BRAND </td>
                    <td> ${mobile.brand} </td>
                </tr>
                <tr>
                    <td>3</td>
                    <td> COLOR </td>
                    <td> ${mobile.color} </td>
                </tr>
                <tr>
                    <td>4</td>
                    <td> PRICE </td>
                    <td> ${mobile.price} </td>
                </tr>
            </tbody>
        </table> `
    document.querySelector('#json-card').innerHTML = jsont;
};

//API BUTTON 
let apiButton = document.querySelector('#api-btn');
apiButton.addEventListener('click', function(){
    //AJAX Call
    let xhr = new XMLHttpRequest();
    //process the ajax
    xhr.open('GET', 'https://jsonplaceholder.typicode.com/users', true)
    //send 
    xhr.send();
    //response 
    xhr.onload = () =>{
        if (xhr.status===200){
          let data = xhr.responseText;
          let jsondata = JSON.parse(data)
          displayUsers(jsondata)
          
        }
    }
});

//Display the jsondata

let displayUsers = (jsondata) => {
   
    let users = 
        `<table class="table table-striped" style="color:brown"> 
            <thead>
               <tr>
                    <th> ID  </th>
                    <th> NAME  </th>
                    <th> USERNAME  </th>
                    <th> EMAIL  </th>
                    <th> STREET  </th>
                    <th> PHONE  </th>
                    <th> WEBSITE  </th>

               </tr>
            </thead>
            <tbody> `
            for(let u of jsondata ){
                users +=
                `
                <tr>
                    <td> ${u.id}</td>
                    <td>  ${u.name}</td>
                    <td>  ${u.username}</td>
                    <td>  ${u.email}</td>
                    <td>  ${u.address.street}</td>
                    <td>  ${u.phone}</td>
                    <td>  ${u.website}</td>
                </tr>  `
            }
            `
            </tbody>
        </table>`
            

    // for(let u of jsondata ){
    //     users += ` <ul class='list-group mt-2'>  
    //         <li class='list-group-item'>  ID: ${u.id} </li>
    //         <li class='list-group-item'>  NAME: ${u.name} </li>
    //         <li class='list-group-item'>  USERNAME: ${u.username} </li>
    //         <li class='list-group-item'>  EMAIL: ${u.email} </li>
    //         <li class='list-group-item'>  STREET: ${u.address.street} </li>
    //         <li class='list-group-item'>  CITY: ${u.address.city} </li>
    //         <li class='list-group-item'>  SUIT: ${u.address.suit} </li>
    //         <li class='list-group-item'>  ZIPCODE: ${u.address.zipcode} </li>
    //         <li class='list-group-item'>  LAT: ${u.address.geo.lat} </li>
    //         <li class='list-group-item'>  LNG: ${u.address.geo.lng} </li>
            
    //     </ul>`
    // } 
    document.querySelector('#api-card').innerHTML=users
}
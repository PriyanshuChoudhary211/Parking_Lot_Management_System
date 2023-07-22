// To Create the Leaderboard Barchart
const ctx = document.getElementById('myChart');

// The list of Registered Users
// var userList=[{user:'UK 08 AF 2023',ArrivalTime:'12:30',DepartureTime:'01:30',Amount:500},
//             {user:'UP 17 B 1203',ArrivalTime:'11:00',DepartureTime:'04:00',Amount:1000},
//             {user:'PB 11 OT 5234',ArrivalTime:'08:50',DepartureTime:'10:00',Amount:1200},
//             {user:'RJ 07 DS 8392',ArrivalTime:'01:20',DepartureTime:'05:00',Amount:800},   
//             {user:'UK 17 F 1991',ArrivalTime:'09:20',DepartureTime:'02:00',Amount:700},
//             {user:'MH 12 ZA 9090',ArrivalTime:'10:45',DepartureTime:'06:00',Amount:1500},
//             {user:'GU 03 DT 2553',ArrivalTime:'05:40',DepartureTime:'07:55',Amount:1256},
//             {user:'UK 17 TT 0001',ArrivalTime:'11:30',DepartureTime:'12:00',Amount:1523},
//             {user:'DL 01 FD 1000',ArrivalTime:'9:00',DepartureTime:'12:45',Amount:2023},
//             {user:'MH 24 GH 1010',ArrivalTime:'12:00',DepartureTime:'01:50',Amount:1020},
//             {user:'AP 12 T 9080',ArrivalTime:'12:45',DepartureTime:'08:10',Amount:1221},
            
//         ]

// var userList='{{ userList }}';

// Sort the User's List
// function sort(userList){
//     for(var i = 0;i<userList.length-1;i++)
//     {
//         for(var j=0;j<userList.length-i-1;j++)
//         {
//             if(userList[j].ArrivalTime>userList[j+1].ArrivalTime)
//             {
//                 var temp=userList[j].ArrivalTime;
//                 userList[j].ArrivalTime=userList[j+1].ArrivalTime;
//                 userList[j+1].ArrivalTime=temp;
//             }
//         }
//     }
//     return userList;
// }

// Printing Table function
function printTable(userList)
{
    var tableuserList=document.getElementById('table');
    var table='<table><thead><tr><th>S.No.</th><th>Plate Number</th><th>Arrival Time</th><th>Leave Time</th><th>Amount</th></tr></thead><tbody>';
    // userList = sort(userList);
    for(var i = 0;i<userList.length;i++)
    {
        table+='<tr><td>'+(i+1)+'</td><td>'+userList[i].user +'</td><td>'+userList[i].ArrivalTime+'</td><td>'+userList[i].DepartureTime+'</td><td>'+userList[i].Amount+'</td></tr>';
    }
    table+='</tbody></table>';

    tableuserList.innerHTML=table;
}

// Settting the rank of users and Printing the table for first time
// function setRank(){
//     userList = sort(userList);
//     for(var i=0;i<userList.length;i++){
//         userList[i].Rank = i+1;
//     }
//     printTable(userList);
// }


// Search Function
function search(userList,value){
    var new_userList = [];
    var len = value.length;
    value = value.toLowerCase();
    for(var i=0;i<userList.length;i++){
        var subs = userList[i].user.substring(0,len).toLowerCase();
        if(subs == value){
            new_userList.push(userList[i]);
        }
    }
    console.log(new_userList[0]);
    return new_userList;
}


// set Leaderboard 
function setLeaderboard(userList){
    var tops = listOfDates;
    // userList = sort(userList);
    // for(var i=0;i<;i++){
    //     tops.push(userList[i].user);
    // }
    new Chart(ctx, {
        type: 'bar',
        data: {
          labels: tops,
          datasets: [{
            // label: '# of Votes',
            data: [1200, 800, 3000,2150,600,1800,860],
            backgroundColor:[
                '#2e597c',
                '#2e597c',
                '#2e597c',
                '#2e597c',
                '#2e597c',
                '#2e597c',
                '#2e597c'
            ],
            borderColor:[
                '#32628a',
                '#32628a',
                '#32628a',
                '#32628a',
                '#32628a',
                '#32628a',
                '#32628a',
            ],
            borderWidth: 1,
          }],
          
        },
        options: {

            plugins: {
                legend: {
                  display: false
                },
                title: {
                    display: true,
                    text: 'Last 7 days Earning',
                    color: 'Black',
                    position: 'top',
                    align: 'center',
                    font: {
                       weight: 'bold',
                       size: 24,
                    },
                    padding: 8,
                    fontSize:20,
                   
                 }
              },          
         }
      });
}



// Set Counters and percentage
function setUsersCount(userList){
    var showup=document.getElementById('showUsers');
    var total=20;  // Consider 2 extra users that are inactive by default
    var active=0; // Consider 2 extra users that are inactive by default
    var currentDate = new Date();
    var currentHour=currentDate.getHours();
    if(currentHour<=9) currentHour='0'+currentHour;
    var currentMin=currentDate.getMinutes();
    if(currentMin<=9) currentMin='0'+currentMin;
    var currentTime=currentHour+":"+currentMin;
    for(var i=0;i<userList.length;i++)
    {
        if(currentTime>=userList[i].ArrivalTime && currentTime<=userList[i].DepartureTime)
        {
            active++;
        }
    }
    if(active<10) active='0'+active;
    var inactive=total-active;
    if(inactive<10) inactive='0'+inactive;
    var totalUser='<span>Total Slots :'+total+'</span><br><span>Slots Filled :'+active+'</span><br><span>Slots Available :'+inactive+'</span>';
    showup.innerHTML=totalUser;


    var percen = Math.floor((active/total)*100);
    var degrees = Math.floor((active/total)*180);
    var perObj = document.getElementById('percentage');
    perObj.innerHTML=percen+'%';

    $('.circle-wrap .circle .mask.full').css('transform','rotate('+degrees+'deg)');
    $('.circle-wrap .circle .fill').css('transform','rotate('+degrees+'deg)');
    document.documentElement.style.setProperty('--degree-end', degrees+'deg');
}



// to filter the search results
$('#user').on("keyup",function(){
    var value = $(this).val();
    var filter_data = search(userList,value);
    printTable(filter_data);
})

// Initialize the Dashboard
function initializeDashboard(userList){
    setUsersCount(userList);
    setLeaderboard(userList);
    printTable(userList);
    // setRank(userList);
}

// Calling main fuction
initializeDashboard(userList);





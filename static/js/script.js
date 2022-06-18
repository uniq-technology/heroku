

let mainPassword = "ffnrxhpykdbdsftt"
let mainMail = "cropdoctor2022@yahoo.com"


function sendEmail() {
  var name = document.getElementById("name").value
  var mail = document.getElementById("mail-id").value
  var address = document.getElementById("address").value
  var contact = document.getElementById("contact").value
  var problem = document.getElementById("problem").value
  var compiler = "Hello, Sir. I am : " + name + ". I am from : " + address + ", here is my email : " + mail + " and contact number : " + contact +
    " . reason for contact is : " + problem + " and I liked your Website."
  alert("Please wait...")
  Email.send({
      Host: "smtp.mail.yahoo.com",
      Username: mainMail,
      Password: mainPassword,
      To: "Pradeepmech01@gmail.com",
      From: mainMail,
      Subject: name,
      Body: compiler,
    })
    .then(function() {
      document.getElementById("name").value = ""
      document.getElementById("mail-id").value = ""
      document.getElementById("contact").value = ""
      document.getElementById("address").value = ""
      document.getElementById("problem").value = ""
      alert("mail sent successfully")
    });
}

// like and dislike


$(".like").click(function() {
  $(this).toggleClass("green")
  $(this).next().removeClass("red");
})

$(".dislike").click(function() {
  $(this).toggleClass("red")
  $(this).prev().removeClass("green");
})

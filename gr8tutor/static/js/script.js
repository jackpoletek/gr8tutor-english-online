document.addEventListener("DOMContentLoaded", function () {

  /* Sticky Navbar */
  const navbar = document.querySelector(".navbar");

  if (navbar) {
    window.addEventListener("scroll", function () {
      if (!navbar) return;

      if (window.scrollY > 50) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  }

  /* Back to Top Button */
  const backToTop = document.querySelector(".back-to-top");

  if (backToTop) {
    window.addEventListener("scroll", function () {
      if (window.scrollY > 300) {
        backToTop.classList.add("show");
      } else {
        backToTop.classList.remove("show");
      }
    });

    backToTop.addEventListener("click", function (e) {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }

  /* Image Slider */
  const sliders = document.querySelectorAll(".image-slider");

  sliders.forEach(function (slider) {
    const images = slider.querySelectorAll(".slider-image");
    const prevBtn = slider.querySelector(".prev");
    const nextBtn = slider.querySelector(".next");
    const dots = slider.querySelectorAll(".slider-dot");

    let currentIndex = 0;

    function updateSlider () {
      slider.querySelector(".slider-images").style.transform = "translateX(-" + (currentIndex * 100) + "%)";

      dots.forEach(function (dot, index) {
        dot.classList.toggle("active", index === currentIndex);
      });
    }

    prevBtn?.addEventListener("click", function () {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
      updateSlider();
    });

    nextBtn?.addEventListener("click", function () {
      currentIndex = (currentIndex + 1) % images.length;
      updateSlider();
    });

    dots.forEach(function (dot, index) {
      dot.addEventListener("click", function () {
        currentIndex = index;
        updateSlider();
      });
    });
  });

  /* Auto-scroll Chat */
  const chatMessages = document.querySelector(".chat-messages");
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  /* Registration Alert & Role Redirect */
  const registerForm = document.getElementById("registerForm");

  if (registerForm) {
    registerForm.addEventListener("submit", function () {
      const selectedRoleInput = document.querySelector('input[name="role"]:checked');
      const selectedRole = selectedRoleInput ? selectedRoleInput.value : "student"; 

      let message = "Thank you for registering on Gr8tutor!\n\n";

      if (selectedRole === "tutor") {
        message +=
          "You registered as a TUTOR.\n\n" +
          "You can now create your tutor profile, offer lessons, and connect with students.";
      } else {
        message +=
          "You registered as a STUDENT.\n\n" +
          "You can now browse tutors, book lessons, and start learning!";
      }

      alert(message);

      setTimeout(function () {
        window.location.href = "/dashboard/";
      }, 500);
    });
  }

  /* Chat Form Validation */
  const chatForms = document.querySelectorAll("form.chat-input");

  chatForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const messageInput = this.querySelector('input[name="message"]');

      if (messageInput && !messageInput.value.trim()) {
        e.preventDefault();
        messageInput.classList.add("is-invalid");
        alert("You cannot send an empty message.");
        messageInput.focus();

        messageInput.addEventListener(
          "input",
          function () {
            this.classList.remove("is-invalid");
          },
          { once: true }
        );
      }
    });
  });

});

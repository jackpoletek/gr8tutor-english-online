document.addEventListener("DOMContentLoaded", function () {
  /* Sticky Navbar */
  const navbar = document.querySelector(".navbar");

  if (navbar) {
    window.addEventListener("scroll", function () {
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
      window.scrollTo({ top: 0, behavior: "smooth" });
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

    function updateSlider() {
      slider.querySelector(".slider-images").style.transform =
        "translateX(-" + currentIndex * 100 + "%)";
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

  /* Reusable SweetAlert helper */
  function showSwal(options) {
    if (typeof Swal !== "undefined") {
      Swal.fire(options);
    } else {
      alert(options.text || "Something went wrong.");
    }
  }

  /* Read Django flags safely */
  const flagsEl = document.getElementById("js-flags");

  if (flagsEl) {
    const loginError = flagsEl.dataset.loginError === "true";
    const loginErrorMessage = flagsEl.dataset.loginErrorMessage;

    const registrationSuccess = flagsEl.dataset.registrationSuccess === "true";
    const registrationMessage = flagsEl.dataset.registrationMessage;

    const registrationError = flagsEl.dataset.registrationError === "true";
    const registrationErrorMessage = flagsEl.dataset.registrationErrorMessage;

    /* Registration success */
    if (registrationSuccess) {
      showSwal({
        icon: "success",
        title: "Registration complete",
        text: registrationMessage || "Thank you for registering on Gr8tutor!",
        confirmButtonText: "Go to login",
      }).then(() => {
        window.location.href = "/login/";
      });
    }

    /* Login error */
    if (loginError) {
      showSwal({
        icon: "error",
        title: "Login failed",
        text: loginErrorMessage || "Invalid login details.",
      });
    }

    /* Registration error */
    if (registrationError) {
      showSwal({
        icon: "error",
        title: "Registration error",
        text: registrationErrorMessage || "Please check the form.",
      });
    }
  }

  /* Chat Form Validation */
  const chatForms = document.querySelectorAll("form.chat-input");

  chatForms.forEach(function (form) {
    form.addEventListener("submit", function (e) {
      const messageInput = this.querySelector('input[name="message"]');

      if (messageInput && !messageInput.value.trim()) {
        e.preventDefault();
        messageInput.classList.add("is-invalid");

        showSwal({
          icon: "warning",
          text: "You cannot send an empty message.",
        });

        messageInput.focus();

        messageInput.addEventListener(
          "input",
          function () {
            this.classList.remove("is-invalid");
          },
          { once: true },
        );
      }
    });
  });
});

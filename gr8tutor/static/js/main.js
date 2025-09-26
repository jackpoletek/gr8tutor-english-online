document.addEventListener("DOMContentLoaded", function () {
  // Sticky Navbar
  const navbar = document.querySelector(".navbar");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // Back to Top Button
  const backToTop = document.querySelector(".back-to-top");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
      backToTop.classList.add("show");
    } else {
      backToTop.classList.remove("show");
    }
  });
  backToTop.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Simple Image Slider
  const sliders = document.querySelectorAll(".image-slider");
  sliders.forEach((slider) => {
    const images = slider.querySelectorAll(".slider-image");
    const prevBtn = slider.querySelector(".prev");
    const nextBtn = slider.querySelector(".next");
    const dots = slider.querySelectorAll(".slider-dot");
    let currentIndex = 0;

    const updateSlider = () => {
      slider.querySelector(".slider-images").style.transform = `translateX(-${
        currentIndex * 100
      }%)`;
      dots.forEach((dot, i) =>
        dot.classList.toggle("active", i === currentIndex)
      );
    };

    prevBtn?.addEventListener("click", () => {
      currentIndex = (currentIndex - 1 + images.length) % images.length;
      updateSlider();
    });

    nextBtn?.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % images.length;
      updateSlider();
    });

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        currentIndex = i;
        updateSlider();
      });
    });

    // Show slider once initialized
    slider.style.display = "block";
  });
});

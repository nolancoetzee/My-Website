 
 
 
 document.addEventListener('DOMContentLoaded', function() {
    // Select the arrow element
    const arrow = document.querySelector('.scroll-arrow');
    // Get the height of the opening section
    const openingHeight = document.getElementById('opening').offsetHeight;

    // Function to hide the arrow when scrolled past the opening section
    function hideArrowOnScroll() {
      if (window.scrollY > openingHeight) {
        arrow.style.display = 'none'; // Hide the arrow
        window.removeEventListener('scroll', hideArrowOnScroll); // Remove the listener
      }
    }

    // Add the scroll event listener
    window.addEventListener('scroll', hideArrowOnScroll);
  });


document.addEventListener("DOMContentLoaded", function() {
    // Select pop-up elements
    const aboutMeButton = document.querySelector('.about-me-button');
    const contactMeButton = document.querySelector('.contact-me-button');
    const popup = document.getElementById('popup');
    const popupOverlay = document.getElementById('popup-overlay');
    const closeButton = document.querySelector('.close-button');
    const aboutMeSection = document.querySelector('.about-me-section');
    const messageForm = document.getElementById('messageForm');
    const sections = document.querySelectorAll('.section'); // Select all elements with class "section"

    // Function to show the pop-up
    function showPopup() {
        popupOverlay.style.display = 'block';
        popup.style.display = 'block';
        sections.forEach(section => {
            section.style.filter = 'blur(5px)'; // Apply blur to all sections
        });
        requestAnimationFrame(() => {
            popup.classList.add('popup-active');
            setTimeout(() => {
                aboutMeSection.classList.add('animate');
            }, 2000);
        });
    }

    // Function to hide the pop-up
    function hidePopup() {
        aboutMeSection.classList.remove('animate');
        popup.classList.remove('popup-active');
        popup.addEventListener('transitionend', function handler() {
            popup.style.display = 'none';
            popupOverlay.style.display = 'none';
            sections.forEach(section => {
                section.style.filter = 'none'; // Remove blur from all sections
            });
            popup.removeEventListener('transitionend', handler);
        }, { once: true });
    }

    // Handle form submission
    messageForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;

        fetch('/api/submit-message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, message })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to submit message');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);
            messageForm.reset();
            hidePopup();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error submitting your message. Please try again.');
        });
    });

    // Add event listeners
    aboutMeButton.addEventListener('click', showPopup);
    contactMeButton.addEventListener('click', showPopup);
    closeButton.addEventListener('click', hidePopup);
});


    //EXPERTISE SECTION

    document.addEventListener("DOMContentLoaded", function() {
      const expertiseSection = document.getElementById("expertise");
      
      // Start with normal state
      expertiseSection.classList.add("normal");
      
      // Intersection Observer to trigger animation on scroll
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              // For screens wider than 768px - do one-time animation
              if (window.innerWidth > 768) {
                // Do initial animation
                expertiseSection.classList.remove("normal");
                expertiseSection.classList.add("animate");
                
                // Return to normal state after animation
                setTimeout(() => {
                  expertiseSection.classList.remove("animate");
                  expertiseSection.classList.add("normal");
                }, 1000);
                
                observer.unobserve(expertiseSection);
              } 
              // For mobile screens (≤768px) - animate, return to normal, then animate permanently
              else {
                // First animation
                expertiseSection.classList.remove("normal");
                expertiseSection.classList.add("animate");
                
                // After 1 second, return to normal
                setTimeout(() => {
                  expertiseSection.classList.remove("animate");
                  expertiseSection.classList.add("normal");
                  
                  // After another 1 second, animate again and stay that way
                  setTimeout(() => {
                    expertiseSection.classList.remove("normal");
                    expertiseSection.classList.add("animate");
                    // No more changes after this - stays animated
                  }, 1000);
                }, 1000);
                
                observer.unobserve(expertiseSection);
              }
            }
          });
        },
        { threshold: 0.5 }
      );
      
      observer.observe(expertiseSection);
    });
    
    function updateScrollAnimation() {
      const elements = document.querySelectorAll('.rectangle');
      if (window.innerWidth <= 768) {
        elements.forEach(element => {
          element.style.animation = 'scroll 1s ease forwards';
          element.style.animationTimeline = 'view()';
          element.style.animationRange = 'entry 0% cover 50%';
        });
      } else {
        elements.forEach(element => {
          element.style.animation = 'none';
          element.style.animationTimeline = '';
          element.style.animationRange = '';
        });
      }
    }
    
    // Handle window resize for expertise section animations
    window.addEventListener('resize', function() {
      const expertiseSection = document.getElementById("expertise");
      if (expertiseSection) {
        if (window.innerWidth <= 768) {
          // When resizing to mobile, if it's in normal state, do the sequence
          if (expertiseSection.classList.contains("normal") && isElementInViewport(expertiseSection)) {
            // First animation
            expertiseSection.classList.remove("normal");
            expertiseSection.classList.add("animate");
            
            // After 1 second, return to normal
            setTimeout(() => {
              expertiseSection.classList.remove("animate");
              expertiseSection.classList.add("normal");
              
              // After another 1 second, animate again and stay that way
              setTimeout(() => {
                expertiseSection.classList.remove("normal");
                expertiseSection.classList.add("animate");
              }, 1000);
            }, 1000);
          }
        } else {
          // When resizing to desktop, return to normal state
          expertiseSection.classList.remove("animate");
          expertiseSection.classList.add("normal");
        }
      }
      
      // Helper function to check if element is in viewport
      function isElementInViewport(el) {
        const rect = el.getBoundingClientRect();
        return (
          rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
          rect.bottom >= 0
        );
      }
    });
    
    window.addEventListener('load', updateScrollAnimation);
    window.addEventListener('resize', updateScrollAnimation);

    










    //MOBILE CODE


    // Function to detect if the user is on a mobile device
    function isMobileDevice() {
      return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    }

    // Function to set the viewport meta tag
    function setViewport() {
      let viewportMeta = document.querySelector('meta[name="viewport"]');

      // If no viewport meta tag exists, create one
      if (!viewportMeta) {
        viewportMeta = document.createElement('meta');
        viewportMeta.name = "viewport";
        document.head.appendChild(viewportMeta);
      }

      if (isMobileDevice()) {
        // Set viewport width to 800px for mobile devices
        viewportMeta.content = "width=768px";
      } else {
        // For non-mobile devices, use a standard responsive setting
        viewportMeta.content = "width=device-width, initial-scale=1.0";
      }
    }

    // Call the function when the page loads
    document.addEventListener('DOMContentLoaded', setViewport);
    // Function to enforce a minimum content width
    function enforceMinWidth() {
      document.body.style.minWidth = '768px';
    }

    // Call the function when the page loads
    document.addEventListener('DOMContentLoaded', enforceMinWidth);


    







    /// ANALYTICS 

    document.addEventListener("DOMContentLoaded", function() {
      // Generate a unique session ID for this visit
      const sessionId = Math.random().toString(36).substring(2, 15);
    
      // Log page view with device type
      fetch('/api/log-page-view', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          device_type: isMobileDevice() ? 'mobile' : 'laptop'
        })
      })
      .then(response => response.json())
      .then(data => console.log(data))
      .catch(error => console.error('Error:', error));
    
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const sectionId = entry.target.id || (entry.target.closest('section') ? entry.target.closest('section').id : null);
          console.log('Section intersecting:', sectionId);
          
          if (sectionId) {
            fetch('/api/log-section-view', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ session_id: sessionId, section: sectionId })
            })
            .then(response => response.json())
            .then(data => console.log('Logged section view:', data))
            .catch(error => console.error('Error logging section view:', error));
            
            observer.unobserve(entry.target);
          }
        }
      });
    }, { threshold: 0.2 });

    document.querySelectorAll('section').forEach(section => {
      observer.observe(section);
    });
    
    document.querySelectorAll('.track-click').forEach(element => {
      element.addEventListener('click', () => {
        // Always get the parent section ID
        const sectionId = element.closest('section') ? element.closest('section').id : 'unknown';
        const elementId = element.id || 'unknown';
        
        if (sectionId) {
          fetch('/api/log-click', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sessionId, section: sectionId, element: elementId })
          })
          .then(response => response.json())
          .then(data => console.log('Logged click:', data))
          .catch(error => console.error('Error logging click:', error));
        }
      });
    });
    
      // Keep your existing form submission code here...
  });
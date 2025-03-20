document.addEventListener("DOMContentLoaded", function() {
    // تحديد العنصر الأب (<h1>) الذي يحتوي على النص
    const learnFunText = document.querySelector("h1");
    
   // تطبيق تأثير GSAP على العنصر الأب
    gsap.from(learnFunText, {
        opacity: 0,
        y: 50,
        duration: 2,
        delay: 0.5,
        ease: "power2.out"
    });

    if (document.body.classList.contains("oe_structure.oe_empty")){
    const bubbleContainer = document.createElement("div");
    bubbleContainer.classList.add("bubble-container");
    document.body.appendChild(bubbleContainer);

    function createBubble() {
        let bubble = document.createElement("div");
        bubble.classList.add("bubble");
        bubble.style.left = Math.random() * 100 + "vw"; // مكان عشوائي أفقيًا
        bubble.style.animationDuration = Math.random() * 3 + 2 + "s"; // مدة حركة عشوائية
        bubbleContainer.appendChild(bubble);

        // إزالة الفقاعة بعد انتهاء الحركة
        setTimeout(() => {
            bubble.remove();
        }, 5000);
    }

    // إنشاء فقاعات جديدة كل نصف ثانية
    setInterval(createBubble, 500);
    }

});
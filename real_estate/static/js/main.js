document.addEventListener("DOMContentLoaded", function () {
  const categorySelect = document.getElementById("id_category");
  const subcategorySelect = document.getElementById("id_subcategory");
  if (categorySelect && subcategorySelect) {
    const subcategories = {
      RES: ["Apartment", "Villa", "Independent House", "Builder Floor"],
      COM: ["Office", "Shop", "Warehouse", "Co-working"],
    };
    const updateSubcategories = () => {
      const cat = categorySelect.value;
      const options = subcategories[cat] || [];
      subcategorySelect.innerHTML = "";
      options.forEach((text) => {
        const opt = document.createElement("option");
        opt.value = text;
        opt.textContent = text;
        subcategorySelect.appendChild(opt);
      });
    };
    categorySelect.addEventListener("change", updateSubcategories);
    updateSubcategories();
  }
});



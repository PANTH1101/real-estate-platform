document.addEventListener("DOMContentLoaded", function () {
  const categorySelect = document.getElementById("id_category");
  const subcategorySelect = document.getElementById("id_subcategory");
  if (categorySelect && subcategorySelect) {
    // Keep JS values in sync with Django model choices:
    // Property.SUBCATEGORY_CHOICES = [
    //   ("APARTMENT", "Apartment"),
    //   ("VILLA", "House / Villa"),
    //   ("PLOT", "Plot / Land"),
    //   ("OFFICE", "Commercial Office"),
    //   ("SHOP", "Shop / Showroom"),
    // ]
    const subcategories = {
      RES: [
        { value: "APARTMENT", label: "Apartment" },
        { value: "VILLA", label: "House / Villa" },
        { value: "PLOT", label: "Plot / Land" },
      ],
      COM: [
        { value: "OFFICE", label: "Commercial Office" },
        { value: "SHOP", label: "Shop / Showroom" },
        { value: "PLOT", label: "Plot / Land" },
      ],
    };
    const updateSubcategories = () => {
      const cat = categorySelect.value;
      const options = subcategories[cat] || [];
      const currentValue = subcategorySelect.value;
      subcategorySelect.innerHTML = "";
      options.forEach(({ value, label }) => {
        const opt = document.createElement("option");
        opt.value = value;
        opt.textContent = label;
        if (value === currentValue) {
          opt.selected = true;
        }
        subcategorySelect.appendChild(opt);
      });
    };
    categorySelect.addEventListener("change", updateSubcategories);
    updateSubcategories();
  }
});



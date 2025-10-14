
document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("restaurant-list");

    // Fetch restaurants from API
    fetch("/api/restaurants/")
        .then(response => response.json())
        .then(data => {
            data.forEach(restaurant => {
                const div = document.createElement("div");
                div.className = "restaurant-card p-4 border rounded m-2 cursor-pointer hover:bg-gray-100";

                div.innerHTML = `
                    <h2 class="font-bold text-lg">${restaurant.name}</h2>
                    <img src="${restaurant.image}" alt="${restaurant.name}" class="w-32 h-32 object-cover">
                    <p>Location: ${restaurant.location}</p>
                    <p>Rating: ${restaurant.rating}</p>
                `;

                // Redirect to restaurant detail page on click
                div.addEventListener("click", () => {
                    window.location.href = `/restaurant/${restaurant.id}/`;
                });

                container.appendChild(div);
            });
        })
        .catch(err => console.error("Error fetching restaurants:", err));
});

// Function to add items to cart from restaurant detail page
function addToCart(id, name, price) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    cart.push({ id, name, price });
    localStorage.setItem("cart", JSON.stringify(cart));
    // Optional: show toast instead of alert
    alert(`${name} added to cart!`);
}

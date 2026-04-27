export const loadGoogleMaps = () => {
  return new Promise((resolve) => {
    if (window.google) return resolve();

    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${import.meta.env.VITE_GOOGLE_MAPS_API_KEY}&libraries=places`;
    console.log(script.src);
    script.async = true;
    script.defer = true;

    script.onload = () => resolve();

    document.head.appendChild(script);
  });
};
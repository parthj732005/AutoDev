// src/utils/safeFetch.jsx
export default async function safeFetch(url, options = {}) {
  try {
    const res = await fetch(url, options);
    return res;
  } catch (err) {
    console.error("Backend unreachable");
    throw err;
  }
}

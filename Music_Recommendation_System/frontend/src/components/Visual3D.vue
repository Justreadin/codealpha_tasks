/* eslint-disable */
<template>
  <div ref="canvasContainer" class="w-full h-96 bg-black"></div>
</template>

<script>
import * as THREE from "three";
import mitt from "mitt";
import logger from "@/utils/logger"; // Ensure you have a logger utility in your project

const emitter = mitt();

export default {
  mounted() {
    const container = this.$refs.canvasContainer;

    if (!container.clientWidth || !container.clientHeight) {
      const errorMessage = "Canvas container has zero dimensions.";
      this.logError(errorMessage); // Log error to backend
      return;
    }

    // Scene
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(
      75,
      container.clientWidth / container.clientHeight,
      0.1,
      8000,
    );

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Music Sphere - Rotating audio-reactive sphere
    const geometry = new THREE.SphereGeometry(2, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0x00ff00,
      emissive: 0x00ff00,
      emissiveIntensity: 0.5,
      wireframe: true,
    });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    // Create a sound-reactive wave effect around the sphere
    const waveGeometry = new THREE.TorusGeometry(2.5, 0.1, 16, 100);
    const waveMaterial = new THREE.MeshBasicMaterial({
      color: 0x00ffff,
      wireframe: true,
    });
    const wave = new THREE.Mesh(waveGeometry, waveMaterial);
    scene.add(wave);

    // Music Notes (floating 3D notes)
    const noteMaterial = new THREE.MeshBasicMaterial({ color: 0xfff000 });
    const noteGeometry = new THREE.OctahedronGeometry(0.1);
    const notes = [];
    for (let i = 0; i < 10; i++) {
      const note = new THREE.Mesh(noteGeometry, noteMaterial);
      note.position.set(
        Math.random() * 6 - 3,
        Math.random() * 3 + 1,
        Math.random() * 6 - 3,
      );
      scene.add(note);
      notes.push(note);
    }

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    const pointLight = new THREE.PointLight(0xffffff, 1, 100);
    pointLight.position.set(5, 5, 5);
    scene.add(ambientLight, pointLight);

    // Set camera position
    camera.position.z = 5;

    // Handle window resizing
    const handleResize = () => {
      const width = container.clientWidth;
      const height = container.clientHeight;

      if (width > 0 && height > 0) {
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
      } else {
        const errorMessage = "Invalid canvas dimensions during resize event.";
        this.logError(errorMessage); // Log error to backend
      }
    };
    window.addEventListener("resize", handleResize);

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);

      // Rotate the sphere and wave for dynamic effect
      sphere.rotation.x += 0.01;
      sphere.rotation.y += 0.01;
      wave.rotation.x += 0.02;
      wave.rotation.y += 0.02;

      // Make music notes float and animate
      notes.forEach((note) => {
        note.position.y += Math.sin(note.position.x * 0.3) * 0.05;
        note.position.x += 0.02;
        if (note.position.x > 3) {
          note.position.x = -3;
        }
      });

      renderer.render(scene, camera);
    };
    animate();

    // Cleanup
    emitter.on("cleanup", () => {
      window.removeEventListener("resize", handleResize);
      renderer.dispose();
    });
  },

  beforeUnmount() {
    emitter.emit("cleanup");
  },

  methods: {
    logError(message) {
      // Log error details to backend (where Winston is set up)
      this.$axios
        .post("http://localhost:8000/log/error", {
          message: message,
          timestamp: new Date().toISOString(),
        })
        .catch((err) => {
          logger.error("Failed to log error:", err);
        });
    },
  },
};
</script>

<style scoped>
/* Canvas container with black background to enhance the visual 3D effect */
::v-deep(div[ref="canvasContainer"]) {
  background: black;
  border-radius: 10px;
  overflow: hidden;
}
</style>

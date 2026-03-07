const { validateData } = require('./validator');

// Pruebas para esquema complejo
console.log('=== PRUEBAS ESQUEMA COMPLEJO ===\n');

// Datos válidos
const validComplexData = {
  user: {
    id: 123,
    profile: {
      firstName: "Ana",
      lastName: "García",
      email: "ana.garcia@example.com",
      phone: "+52551234567",
      birthDate: "1990-05-15"
    },
    preferences: {
      theme: "dark",
      notifications: true,
      language: "es"
    },
    tags: ["developer", "javascript", "node"]
  },
  metadata: {
    createdAt: "2024-01-15T10:30:00Z",
    version: "1.0.0"
  }
};

console.log('Datos válidos complejos:');
const result = validateData(validComplexData);
console.log('Válido:', result.valid);
if (!result.valid) {
  console.log('Errores:', result.errors);
}

console.log('\n=== FIN PRUEBAS ===');
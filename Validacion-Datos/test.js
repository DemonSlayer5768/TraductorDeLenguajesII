const { validateData } = require('./validator');

// Casos de prueba
console.log('=== PRUEBAS DE VALIDACIÓN ===\n');

// Caso 1: Datos válidos completos
const validData = {
  name: "María García",
  email: "maria.garcia@example.com",
  age: 25,
  isActive: true
};

console.log('1. Datos válidos:');
console.log('Entrada:', JSON.stringify(validData, null, 2));
const result1 = validateData(validData);
console.log('Resultado:', result1);
console.log();

// Caso 2: Datos válidos mínimos (solo requeridos)
const minimalData = {
  name: "Juan",
  email: "juan@test.com"
};

console.log('2. Datos mínimos (solo campos requeridos):');
console.log('Entrada:', JSON.stringify(minimalData, null, 2));
const result2 = validateData(minimalData);
console.log('Resultado:', result2);
console.log();

// Caso 3: Email inválido
const invalidEmail = {
  name: "Pedro López",
  email: "pedro-invalid-email"
};

console.log('3. Email inválido:');
console.log('Entrada:', JSON.stringify(invalidEmail, null, 2));
const result3 = validateData(invalidEmail);
console.log('Resultado:', result3);
console.log();

// Caso 4: Nombre demasiado largo
const longName = {
  name: "Este es un nombre que definitivamente es mucho más largo de lo permitido por el esquema de validación",
  email: "test@example.com"
};

console.log('4. Nombre demasiado largo:');
console.log('Entrada:', JSON.stringify(longName, null, 2));
const result4 = validateData(longName);
console.log('Resultado:', result4);
console.log();

// Caso 5: Edad negativa
const negativeAge = {
  name: "Ana Ruiz",
  email: "ana@example.com",
  age: -10
};

console.log('5. Edad negativa:');
console.log('Entrada:', JSON.stringify(negativeAge, null, 2));
const result5 = validateData(negativeAge);
console.log('Resultado:', result5);
console.log();

// Caso 6: Falta campo requerido
const missingRequired = {
  email: "solo@email.com"
};

console.log('6. Falta campo requerido (name):');
console.log('Entrada:', JSON.stringify(missingRequired, null, 2));
const result6 = validateData(missingRequired);
console.log('Resultado:', result6);
console.log();

// Caso 7: Tipo de dato incorrecto
const wrongType = {
  name: "Carlos",
  email: "carlos@example.com",
  age: "treinta", // Debería ser número
  isActive: "yes" // Debería ser boolean
};

console.log('7. Tipos de dato incorrectos:');
console.log('Entrada:', JSON.stringify(wrongType, null, 2));
const result7 = validateData(wrongType);
console.log('Resultado:', result7);
console.log();

console.log('=== FIN DE PRUEBAS ===');
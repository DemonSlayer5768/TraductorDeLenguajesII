const fs = require('fs');
const path = require('path');

/**
 * Traductor de Esquemas a Código de Validación JavaScript
 * Genera código funcional usando Ajv para validar datos según un esquema JSON Schema
 */

// Leer el esquema desde archivo
function loadSchema(schemaPath) {
  try {
    const schemaData = fs.readFileSync(schemaPath, 'utf8');
    return JSON.parse(schemaData);
  } catch (error) {
    console.error('Error al cargar el esquema:', error.message);
    process.exit(1);
  }
}

// Generar código JavaScript para validación
function generateValidatorCode(schema) {
  const schemaString = JSON.stringify(schema, null, 2);

  return `const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const ajv = new Ajv({ allErrors: true, verbose: true });
addFormats(ajv);

// Esquema de validación
const schema = ${schemaString};

// Compilar el esquema
const validate = ajv.compile(schema);

/**
 * Función para validar datos según el esquema
 * @param {Object} data - Los datos a validar
 * @returns {Object} - Resultado de la validación
 */
function validateData(data) {
  const valid = validate(data);

  if (valid) {
    return {
      valid: true,
      message: 'Datos válidos'
    };
  } else {
    return {
      valid: false,
      errors: validate.errors.map(error => ({
        field: error.dataPath,
        message: error.message,
        keyword: error.keyword,
        params: error.params
      }))
    };
  }
}

// Exportar la función de validación
module.exports = { validateData, schema };

// Ejemplo de uso (descomentar para probar)
if (require.main === module) {
  // Datos de ejemplo
  const testData = {
    name: "Juan Pérez",
    email: "juan@example.com",
    age: 30,
    isActive: true
  };

  console.log('Validando datos de ejemplo:');
  console.log(JSON.stringify(testData, null, 2));
  console.log('\\nResultado:');
  console.log(validateData(testData));

  // Datos inválidos
  const invalidData = {
    name: "",
    email: "invalid-email",
    age: -5
  };

  console.log('\\nValidando datos inválidos:');
  console.log(JSON.stringify(invalidData, null, 2));
  console.log('\\nResultado:');
  console.log(validateData(invalidData));
}
`;
}

// Función principal
function main() {
  const args = process.argv.slice(2);
  const schemaFile = args[0] || 'schema.json';
  const schemaPath = path.join(__dirname, schemaFile);
  const outputPath = path.join(__dirname, 'validator.js');

  console.log('Cargando esquema desde:', schemaPath);
  const schema = loadSchema(schemaPath);

  console.log('Generando código de validación...');
  const code = generateValidatorCode(schema);

  console.log('Escribiendo código en:', outputPath);
  fs.writeFileSync(outputPath, code, 'utf8');

  console.log('✅ Traducción completada exitosamente!');
  console.log('Ejecuta: node validator.js para probar la validación');
  console.log('Ejecuta: npm test para ejecutar pruebas');
}

// Ejecutar si se llama directamente
if (require.main === module) {
  main();
}

module.exports = { generateValidatorCode, loadSchema };

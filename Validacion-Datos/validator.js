const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const ajv = new Ajv({ allErrors: true, verbose: true });
addFormats(ajv);

// Esquema de validación
const schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "minLength": 1,
      "maxLength": 50
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "age": {
      "type": "integer",
      "minimum": 0,
      "maximum": 120
    },
    "isActive": {
      "type": "boolean"
    }
  },
  "required": [
    "name",
    "email"
  ]
};

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
  console.log('\nResultado:');
  console.log(validateData(testData));

  // Datos inválidos
  const invalidData = {
    name: "",
    email: "invalid-email",
    age: -5
  };

  console.log('\nValidando datos inválidos:');
  console.log(JSON.stringify(invalidData, null, 2));
  console.log('\nResultado:');
  console.log(validateData(invalidData));
}

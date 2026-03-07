# Traductor de Validación de Datos

## Descripción

Este proyecto implementa un traductor especializado en la validación automática de datos en JavaScript mediante esquemas definidos previamente. Utiliza bibliotecas populares como Ajv para generar código funcional que valida estructuras de datos complejas según especificaciones JSON Schema.

## Características

- **Traducción automática**: Convierte esquemas JSON Schema en código JavaScript ejecutable
- **Validación robusta**: Usa Ajv con soporte completo para JSON Schema
- **Formatos extendidos**: Soporte para formatos como email, fechas, etc. mediante ajv-formats
- **Mensajes de error detallados**: Proporciona errores específicos con campo, mensaje y parámetros
- **Fácil integración**: Código generado es modular y reutilizable

## Tecnologías

- **JavaScript/Node.js**: Lenguaje de implementación
- **Ajv**: Biblioteca principal para validación JSON Schema
- **ajv-formats**: Extensión para formatos adicionales
- **JSON Schema**: Estándar para definición de esquemas

## Instalación

```bash
npm install
```

## Uso

1. **Definir esquema**: Crear un archivo `schema.json` con la definición JSON Schema
2. **Generar validador**: Ejecutar `node main.js` para generar `validator.js`
3. **Usar validador**: Ejecutar `node validator.js` para probar o integrar en tu aplicación

## Ejemplo

### Esquema (schema.json)
```json
{
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
    }
  },
  "required": ["name", "email"]
}
```

### Código generado (validator.js)
```javascript
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const ajv = new Ajv({ allErrors: true, verbose: true });
addFormats(ajv);

const schema = { ... }; // Tu esquema

const validate = ajv.compile(schema);

function validateData(data) {
  const valid = validate(data);
  return valid ? { valid: true, message: 'Datos válidos' } :
                 { valid: false, errors: validate.errors };
}

module.exports = { validateData, schema };
```

### Uso en aplicación
```javascript
const { validateData } = require('./validator');

const result = validateData({
  name: "Juan Pérez",
  email: "juan@example.com",
  age: 30
});

if (result.valid) {
  console.log("Datos válidos");
} else {
  console.log("Errores:", result.errors);
}
```

## Beneficios

- **Automatización**: Reduce tiempo de desarrollo de validaciones
- **Estandarización**: Usa estándares JSON Schema ampliamente adoptados
- **Flexibilidad**: Soporte para múltiples bibliotecas (Ajv, Zod, Joi)
- **Extensibilidad**: Fácil agregar nuevos formatos o reglas personalizadas
- **Integridad de datos**: Garantiza calidad y consistencia de datos

## Casos de Uso

- Validación de formularios web
- APIs REST con validación de entrada
- Procesamiento de datos en servicios backend
- Validación de configuraciones
- Integración con bases de datos

## Desarrollo Futuro

- Soporte para Zod y Joi
- Interfaz web para definición visual de esquemas
- Generación de código para otros lenguajes
- Integración con frameworks como Express.js
- Validación en tiempo real

## Contribución

Este proyecto es educativo y permite implementaciones personalizadas según intereses específicos del desarrollador.
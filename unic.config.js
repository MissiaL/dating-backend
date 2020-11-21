module.exports = {
  dynamic: {
    name: process.env['CI_PROJECT_NAME'],
    namespace: process.env['CI_PROJECT_NAMESPACE'],
    type: 'dynamic',
    environment: 'dev',
    services: [
      {
        name: 'app',
        resources: {
          preset: 'nodejs-microservice',
        },
         ports: {
             external: 80,
             internal: 4000
           },

        env: {},
      },
    ],
  },
  prod: {
    name: process.env['CI_PROJECT_NAME'],
    namespace: process.env['CI_PROJECT_NAMESPACE'],
    type: 'prod',
    environment: 'dev',
    services: [
      {
        name: 'app',
        resources: {
          preset: 'nodejs-microservice',
        },
        env: {},
      },
    ],
  },
};

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

        env: {
          'POSTGRES_HOST':'m1-pg-hackecosystem.devops.tcsbank.ru',
          'POSTGRES_USERNAME':'hackecosystem',
          'POSTGRES_PASSWORD':process.env['POSTGRES_PASSWORD'],
        },
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

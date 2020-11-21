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
          'APP_DOMAIN_NAME': `https://${process.env['CI_PROJECT_NAME']}.hackecosystem.dev2.k8s.tcsbank.ru`,
          'APP_DOMAIN_PORT': 80,
          'POSTGRES_HOST':process.env['POSTGRES_HOST'],
          'POSTGRES_USERNAME':process.env['POSTGRES_USERNAME'],
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
        env: {
          'POSTGRES_HOST':process.env['POSTGRES_HOST'],
          'POSTGRES_USERNAME':process.env['POSTGRES_USERNAME'],
          'POSTGRES_PASSWORD':process.env['POSTGRES_PASSWORD'],
        },
      },
    ],
  },
};

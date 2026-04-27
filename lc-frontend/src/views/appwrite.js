import { Client, Account} from 'appwrite';

export const client = new Client();

client
    .setEndpoint('https://Frankfurt.cloud.appwrite.io/v1')
    .setProject('moop'); // Replace with your project ID

export const account = new Account(client);
export { ID } from 'appwrite';
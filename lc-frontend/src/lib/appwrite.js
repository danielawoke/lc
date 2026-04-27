import { Client, Account } from "appwrite";

const client = new Client()
  .setEndpoint("https://fra.cloud.appwrite.io/v1")
  .setProject("69a377280023d14ba4d2");

export const AccountLocal = new Account(client);
# Alert & Monitoring Agent

A general-purpose Alert & Monitoring Agent based on Fetch.AI's uAgents framework.

## Set Up Instructions


## Architecture

Instead of a simple Temperature Alert Agent, we generalized the problem to being able to have alerts for any time-series data. For this, we imagined uAgents as microservices:

![image](https://github.com/sudoshreyansh/Alert-Monitoring-Agent/assets/44190883/b17ef490-1b05-4c13-91ae-e5c5cf50b8a6)

- **Frontend:** The user-facing UI
- **Multiplexed HTTP Server & uAgent:** We multiplexed HTTP Server and uAgent in the frontend-facing backend. This is to allow both communication through HTTP clients and uAgents.
- **Alert uAgent:** The Alert Agent and Protocol allows for continuous monitoring and alerts of any time-series data as requested.
- **Source uAgent:** The Source Agent and Protocol allows query of time-series data provided to the Alert Agent. This can be replaced to be any provider like Temperature data, Currency Exchange Rate data, etc.
- **Notification uAgent:** The Notification uAgent and Protocol allow notifications to users through multiple streams.

The user data is stored in the Multiplexed Backend and forwarded to other uAgents partially only when required, thus preserving privacy. This architecture allows for a dynamic architecture and quick plug-and-play mechanisms which is essential for a decentralized ecosystem.

In this project, we have the Source uAgent = Open Weather Map API, and the Notifications Agent = Twilio SMS Service.

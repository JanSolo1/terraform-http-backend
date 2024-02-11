# Terraform HTTP Backend with Flask

This Flask application was created to serve as a private HTTP backend for Terraform. The motivation behind this project was to have a secure environment in a home lab setup where Terraform state data can be stored. This solution provides an alternative to relying on public cloud providers or other third-party services for state management.

## Requirements

Before running the application, you need to install the required Python packages. These are listed in the `requirements.txt` file. You can install them using pip:

```bash
pip install -r requirements.txt
```
> Note: You can also use systemd usage if you don't want to bother with a manual setup

## How to Use

The application provides several endpoints that Terraform can interact with to manage state data:

- `GET /terraform/state`: Retrieves the current state data.
- `POST /terraform/state`: Updates the current state data with new data.
- `GET /terraform/lock`: Checks whether the state data is currently locked.
- `POST /terraform/lock`: Locks the state data to prevent other operations from modifying it.
- `POST /terraform/unlock`: Unlocks the state data to allow other operations to modify it.

To use this application as your Terraform backend, you need to configure Terraform to use an HTTP backend and point it to the URL where this application is running. Here's an example of how to do this in your Terraform configuration:

```terraform
terraform {
  backend "http" {
    address = "http://<your-server-ip>:<your-server-port>/terraform/state"
    lock_address = "http://<your-server-ip>:<your-server-port>/terraform/lock"
    unlock_address = "http://<your-server-ip>:<your-server-port>/terraform/unlock"
  }
}
```

Replace `<your-server-ip>` and `<your-server-port>` with the IP address or hostname and port of the server where this Flask application is running.
```py
if __name__ == '__main__':
    app.run(host='<your-ip>', port=<your-port>, debug=True) 
```

## systemd usage
Clone the repo:
```bash
git clone https://github.com/yourusername/yourrepository.git
```

cd into the repo:
```bash
cd terraform-http-backend
```

install the server:
```bash
sh create_service.sh
```

>Note: to check if it's runnung, use: `systemctl status http_server.service`

Once you've set up your Terraform configuration, you can run `terraform init` to initialize your backend. After that, you can use Terraform as you normally would, and it will store its state data in your private backend.

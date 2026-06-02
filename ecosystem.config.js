module.exports = {
  apps: [
    {
      name: "vext-agents-orchestrator",
      script: "./venv/bin/python",
      args: "agents/run_all_agents.py",
      cwd: "/opt/vext-audit",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      error_file: "./logs/pm2_error.log",
      out_file: "./logs/pm2_out.log",
      env: {
        PYTHONPATH: ".",
        PYTHONUNBUFFERED: "1"
      }
    },
    {
      name: "vext-api-gateway",
      script: "./venv/bin/uvicorn",
      args: "app.main:app --host 0.0.0.0 --port 8000 --workers 4",
      cwd: "/opt/vext-audit",
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: "1G",
      log_date_format: "YYYY-MM-DD HH:mm:ss Z",
      error_file: "./logs/api_error.log",
      out_file: "./logs/api_out.log",
      env: {
        PYTHONPATH: ".",
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
};


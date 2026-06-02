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
    }
  ]
};

import sys
import json
import logging
from backend.rag.engine import RAGEngine

# Basic MCP Server implementation over Stdio
# Protocol Reference: Model Context Protocol

class MCPServer:
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.logger = logging.getLogger("mcp_server")
        logging.basicConfig(filename="mcp_server.log", level=logging.INFO)

    def run(self):
        self.logger.info("Starting MCP Server...")
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                request = json.loads(line)
                self.handle_request(request)
            except Exception as e:
                self.logger.error(f"Error processing request: {e}")
                sys.stdout.flush()

    def handle_request(self, request):
        method = request.get("method")
        msg_id = request.get("id")
        
        response = {
            "jsonrpc": "2.0",
            "id": msg_id
        }

        if method == "initialize":
            response["result"] = {
                "protocolVersion": "0.1.0",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "MedBot",
                    "version": "1.0.0"
                }
            }
        elif method == "tools/list":
            response["result"] = {
                "tools": [
                    {
                        "name": "query_medbot",
                        "description": "Query the Medical AI Agent about treatment options and clinical trials.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "The medical query to answer."},
                                "patient_id": {"type": "string", "description": "Optional patient ID for context."}
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})
            
            if tool_name == "query_medbot":
                query_text = args.get("query")
                patient_id = args.get("patient_id")
                
                result = self.rag_engine.query(query_text, patient_id)
                
                response["result"] = {
                    "content": [
                        {
                            "type": "text",
                            "text": result
                        }
                    ]
                }
            else:
                response["error"] = {"code": -32601, "message": "Method not found"}
        else:
             # Basic implementation implies ignoring notifications or unknown methods for now
             # But strictly we should return method not found
             pass
        
        if "result" in response or "error" in response:
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    server = MCPServer()
    server.run()

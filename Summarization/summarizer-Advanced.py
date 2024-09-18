# File: function_summarizer.py
import ast
import os

class FunctionSummarizer(ast.NodeVisitor):
    def __init__(self, file_path):
        self.summaries = []
        self.code_snippets = []
        self.ast_trees = []
        self.file_path = file_path  # Store the file path

    def visit_FunctionDef(self, node):
        function_name = node.name
        arguments = [arg.arg for arg in node.args.args]
        
        # Get the docstring if available
        docstring = ast.get_docstring(node)
        doc_summary = f" Docstring: {docstring}" if docstring else " No docstring available."
        
        # Summarize function
        summary = f"Function '{function_name}' takes {len(arguments)} arguments: {', '.join(arguments)}. {doc_summary}"
        self.summaries.append((function_name, summary))
        
        # Extract code snippet
        with open(self.file_path, 'r', encoding='utf-8') as source_file:
            code_snippet = ast.get_source_segment(source_file.read(), node)
        self.code_snippets.append((function_name, code_snippet))

        # Store the AST for future use
        self.ast_trees.append((function_name, ast.dump(node, annotate_fields=True, include_attributes=True)))
        
        # Continue visiting other nodes
        self.generic_visit(node)

def summarize_functions_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())
        summarizer = FunctionSummarizer(file_path)  # Pass the file path to the summarizer
        summarizer.visit(tree)
        return summarizer.summaries, summarizer.code_snippets, summarizer.ast_trees

def summarize_functions_in_directory(directory_path):
    all_summaries = {}
    all_code_snippets = {}
    all_asts = {}
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                summaries, code_snippets, asts = summarize_functions_in_file(file_path)
                all_summaries[file] = summaries
                all_code_snippets[file] = code_snippets
                all_asts[file] = asts
                
    return all_summaries, all_code_snippets, all_asts

def save_to_files(summary_file, snippet_file, ast_file, function_summaries, code_snippets, ast_trees):
    # Save function summaries
    with open(summary_file, 'w', encoding='utf-8') as f:
        for file, summaries in function_summaries.items():
            f.write(f"\nFile: {file}\n")
            for function, summary in summaries:
                f.write(f" - {summary}\n")
    
    # Save code snippets
    with open(snippet_file, 'w', encoding='utf-8') as f:
        for file, snippets in code_snippets.items():
            f.write(f"\nFile: {file}\n")
            for function, snippet in snippets:
                f.write(f"\nFunction: {function}\nCode:\n{snippet}\n")
    
    # Save ASTs
    with open(ast_file, 'w', encoding='utf-8') as f:
        for file, trees in ast_trees.items():
            f.write(f"\nFile: {file}\n")
            for function, tree in trees:
                f.write(f"\nFunction: {function}\nAST:\n{tree}\n")

if __name__ == "__main__":
    project_dir = "Python"  # Change this to your project directory
    summaries_file = "function_summaries.txt"
    snippets_file = "code_snippets.txt"
    asts_file = "function_asts.txt"

    function_summaries, code_snippets, ast_trees = summarize_functions_in_directory(project_dir)
    
    # Save the summaries, code snippets, and ASTs to separate files
    save_to_files(summaries_file, snippets_file, asts_file, function_summaries, code_snippets, ast_trees)
    
    print(f"Function summaries, code snippets, and ASTs have been saved to separate files.")

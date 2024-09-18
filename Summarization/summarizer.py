import ast
import os

class FunctionSummarizer(ast.NodeVisitor):
    def __init__(self):
        self.summaries = []
        self.ast_trees = []

    def visit_FunctionDef(self, node):
        function_name = node.name
        arguments = [arg.arg for arg in node.args.args]
        
        # Extract the docstring if available
        docstring = ast.get_docstring(node)
        if docstring:
            doc_summary = f" Docstring: {docstring}"
        else:
            doc_summary = " No docstring available."
        
        summary = f"Function '{function_name}' takes {len(arguments)} arguments: {', '.join(arguments)}. {doc_summary}"
        self.summaries.append((function_name, summary))
        
        # Store the AST for future use
        self.ast_trees.append((function_name, ast.dump(node, annotate_fields=True, include_attributes=True)))
        
      
        self.generic_visit(node)

def summarize_functions_in_file(file_path):
    with open(file_path, "r", encoding="utf-8") as source:
        tree = ast.parse(source.read())
        summarizer = FunctionSummarizer()
        summarizer.visit(tree)
        return summarizer.summaries, summarizer.ast_trees

def summarize_functions_in_directory(directory_path):
    summaries = {}
    asts = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_summaries, file_asts = summarize_functions_in_file(file_path)
                summaries[file] = file_summaries
                asts[file] = file_asts
    return summaries, asts

def save_summaries_to_file(file_path, function_summaries, ast_trees):
    with open(file_path, 'w', encoding='utf-8') as f:
        for file, summaries in function_summaries.items():
            f.write(f"File: {file}\n")
            for function, summary in summaries:
                f.write(f" - {summary}\n")
            f.write("\n")
        
       
        f.write("\n=== Abstract Syntax Trees (ASTs) ===\n")
        for file, trees in ast_trees.items():
            f.write(f"\nFile: {file} ASTs\n")
            for function, tree in trees:
                f.write(f"Function: {function}\nAST: {tree}\n")


if __name__ == "__main__":
    project_dir = "Python"  
    output_file = "function_summaries.txt"  # File to save the summaries and ASTs

    function_summaries, ast_trees = summarize_functions_in_directory(project_dir)
    
    # Save the summaries and ASTs to a file
    save_summaries_to_file(output_file, function_summaries, ast_trees)
    
    print(f"Function summaries and ASTs have been saved to {output_file}")

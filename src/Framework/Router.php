<?php

declare(strict_types=1);

namespace Framework;

class Router
{
    private array $routes=[];

    public function add(string $method, string $path)
    {
        $path = $this->normalizePath($path);

       $this->routes[] = [
        'path' => $path,
        'method' => strtoupper($method)
       ];
    }
    #getting path, delete first and last '/' if exist adding '/' for both sites
    #for index.php reduce second '/' 
    private function normalizePath(string $path): string
    {
        $path = trim($path, '/');
        $path = "/{$path}/";
        $path = preg_replace('#[/]{2,}#', '/', $path);

        return $path;
    }
}

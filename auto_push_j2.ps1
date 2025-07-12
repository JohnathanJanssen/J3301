cd "C:\Users\Black\OneDrive\Desktop\J2"
git add .
$changes = git status --porcelain
if ($changes) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    git commit -m "Auto-push: Sync at $timestamp"
    git push
}
